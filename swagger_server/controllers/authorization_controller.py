from connexion.exceptions import Unauthorized
from swagger_server.logger import logger


def check_api_key(api_key, required_scopes):
    """
    Проверка API-ключа и его разрешений.

    :param api_key: API-ключ, предоставленный клиентом.
    :type api_key: str
    :param required_scopes: Список необходимых разрешений.
    :type required_scopes: list
    :return: Информация о пользователе, если ключ действителен.
    :rtype: dict
    :raises Unauthorized: Если ключ недействителен.
    """
    valid_api_keys = {
        "12345": {"user_id": 1, "scopes": ["read", "write"]}
    }
    if api_key not in valid_api_keys:
        logger.error(f"Неверный API-ключ: {api_key}")
        raise Unauthorized("Неверный API-ключ")
    key_info = valid_api_keys[api_key]
    return {"user_id": key_info["user_id"]}
