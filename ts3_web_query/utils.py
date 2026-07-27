from urllib.parse import urlencode

from .types.error import TeamSpeakError


def build_request(command: str, params: dict | list | None = None) -> str:
    """
    Builds a full request string from a given command and parameters.

    Parameters
    ----------
    command : str
        The server query command to build.
    params : dict or list or None, optional
        The parameters to pass with the command. If a dict, the parameters will be URL-encoded.
        If a list, the parameters will be joined with '&'. If None, the parameters will be ignored.

    Returns
    -------
    str
        The full request string.
    """
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
        return f"{command}?{param_str}"
    else:
        return f"{command}"


def lprint(args):
    for arg in args:
        print(arg)


def status_to_error(response) -> TeamSpeakError:
    """
    Converts an HttpClient.request() response into a TeamSpeakError.

    On success, commands without a return value have a ``None`` body (JSON
    ``null``), which cannot be unpacked with ``**``. On failure, the response
    is the status dict (``{"code": int, "message": str}``).

    Parameters
    ----------
    response
        The raw value returned by ``HttpClient.request()``.

    Returns
    -------
    TeamSpeakError
        ``TeamSpeakError(code=0, message='ok')`` if response is ``None``,
        otherwise ``TeamSpeakError(**response)``.
    """
    if response is None:
        return TeamSpeakError(code=0, message='ok')
    return TeamSpeakError(**response)

