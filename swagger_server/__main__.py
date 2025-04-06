import re
import threading
import time
import connexion
from flask import request
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from prometheus_client import start_http_server, Counter, Gauge
from sqlalchemy import func
from swagger_server import encoder
from swagger_server.database import db
from swagger_server.logger import logger
from .models import Figure

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


# Создание ресурса с именем сервиса
resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "python_server"
})

# Создание провайдера трейсеров с ресурсом
tracer_provider = TracerProvider(resource=resource)

# Создание экспортера
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4317", insecure=True)

# Создание процессора спанов и добавление его в провайдер
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Установка провайдера трейсеров
trace.set_tracer_provider(tracer_provider)

# Получение трейсеров
tracer = trace.get_tracer(__name__)


def update_endpoint(endpoint, method):
    match = re.match(r"^(.*)/(\d+)$", endpoint)
    if match:
        return match.group(1) + '/' + method
    else:
        if method == 'GET':
            return endpoint + '/GET_ALL'
    return endpoint + '/' + method


REQUEST_COUNT = Counter('http_requests_total',
                        'Total HTTP Requests',
                        ['endpoint', 'method'])
FIGURE_COUNT = Gauge('figures_count',
                     'Total figures count in the database')


def track_requests(app):
    @app.before_request
    def before_request():
        span_name = f"{request.method} {request.path}"
        span = tracer.start_span(span_name)
        request._otel_span = span

        endpoint = request.path
        method = request.method
        if '/figures' in endpoint:
            endpoint = update_endpoint(endpoint, method)
        REQUEST_COUNT.labels(endpoint=endpoint, method=method).inc()

    @app.after_request
    def after_request(response):
        span = getattr(request, '_otel_span', None)
        if span:
            span.end()
        return response


def update_system_metrics(app):
    while True:
        with app.app_context():
            FIGURE_COUNT.set(db.session.query(func.count(Figure.id)).scalar())
        time.sleep(1)


def main():
    # Запуск сервера для экспорта метрик
    start_http_server(8000)

    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml',
                arguments={'title': 'Архив информации о коллекционных фигурках лошадей'},
                pythonic_params=True)

    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///figure.db'
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app.app)

    # Регистрируем middleware для отслеживания запросов
    track_requests(app.app)

    with app.app.app_context():
        db.create_all()

    # Запускаем поток для обновления метрик
    threading.Thread(target=update_system_metrics,
                     args=(app.app,), daemon=True).start()
    logger.info("Запущен поток для обновления метрик")

    logger.info("Сервер запущен")
    app.run(port=5000)


if __name__ == '__main__':
    main()
