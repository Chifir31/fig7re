import connexion
from flask import jsonify
from swagger_server.database import db
from swagger_server.logger import logger
from swagger_server.models.figure import Figure  # noqa: E501


def figures_get():  # noqa: E501
    """Получить список фигурок

     # noqa: E501


    :rtype: List[Figure]
    """
    figures = Figure.query.all()
    return jsonify([figure.to_dict() for figure in figures]), 200


def figures_id_delete(id_):  # noqa: E501
    """Удалить фигурку

     # noqa: E501

    :param id_: ID фигурки
    :type id_: int

    :rtype: None
    """
    figure = Figure.query.get(id_)
    if not figure:
        logger.error("Фигурка не найдена")
        return {"message": "Фигурка не найдена"}, 404

    db.session.delete(figure)
    db.session.commit()
    logger.info("Фигурка успешно удалена")
    return {"message": "Фигурка успешно удалена"}, 204


def figures_id_get(id_):  # noqa: E501
    """Получить фигурку по ID

     # noqa: E501

    :param id_: ID фигурки
    :type id_: int

    :rtype: Figure
    """
    figure = Figure.query.get(id_)
    if figure:
        return jsonify(figure.to_dict()), 200
    logger.error("Фигурка не найдена")
    return {"message": "Фигурка не найдена"}, 404


def figures_id_put(body, id_):  # noqa: E501
    """Обновить фигурку

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id_: ID фигурки
    :type id_: int

    :rtype: Figure
    """
    figure = Figure.query.get(id_)
    if not figure:
        logger.error("Фигурка не найдена")
        return {"message": "Фигурка не найдена"}, 404

    if connexion.request.is_json:
        data = connexion.request.get_json()
        figure.name = data.get('name', figure.name)
        figure.brand = data.get('brand', figure.brand)
        figure.release = data.get('release', figure.release)
        figure.scale = data.get('scale', figure.scale)
        figure.size = data.get('size', figure.size)

        db.session.commit()
        return jsonify(figure.to_dict()), 200

    return {"message": "Неверный формат запроса"}, 400


def figures_post(body):  # noqa: E501
    """Добавить новую фигурку

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Figure
    """
    if connexion.request.is_json:
        data = connexion.request.get_json()
        new_product = Figure(
            name=data.get('name'),
            brand=data.get('brand'),
            release=data.get('release'),
            scale=data.get('scale'),
            size=data.get('size'),
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    return {"message": "Неверный формат запроса"}, 400
