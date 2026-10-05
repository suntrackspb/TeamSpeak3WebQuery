class TeamSpeakException(Exception):
    """Base class of every exception raised by this library."""


class TeamSpeakConnectionError(TeamSpeakException):
    """Raised when the HTTP request to the TS3 WebQuery API fails or returns an unexpected response."""


class TeamSpeakAPIError(TeamSpeakException):
    """
    Raised when the TeamSpeak server answers a command with an error status.

    Attributes:
        code (int): The TeamSpeak error ID, e.g. 2568 (insufficient client permissions).
        message (str): The error message of the server.
        extra_message (str | None): Additional details, e.g. ``failed_permid=17``.
    """

    def __init__(self, code: int, message: str, extra_message: str | None = None):
        self.code = code
        self.message = message
        self.extra_message = extra_message
        text = f'{code} {message}'
        if extra_message:
            text += f' ({extra_message})'
        super().__init__(text)
