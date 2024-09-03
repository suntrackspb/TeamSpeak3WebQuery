from urllib.parse import urlencode


def build_request(command: str, params: dict | list | None = None) -> str:
    if isinstance(params, list):
        # Преобразуем список параметров в строку
        param_str = '&'.join(params)
    elif isinstance(params, dict):
        # Преобразуем словарь параметров в строку с URL-кодировкой
        param_str = urlencode(params)
    else:
        param_str = ''

    # Формируем итоговый запрос
    if param_str:
        return f"/{command}?{param_str}"
    else:
        return f"/{command}"
