from urllib.parse import urlencode


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
        param_str = '&'.join(params)
    elif isinstance(params, dict):
        param_str = urlencode(params)
    else:
        param_str = ''

    if param_str:
        return f"{command}?{param_str}"
    return command
