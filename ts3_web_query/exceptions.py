class TeamSpeakAPIError(Exception):
    """Raised when the TS3 WebQuery API returns a non-zero status code."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class TeamSpeakConnectionError(Exception):
    """Raised when the HTTP request to the TS3 WebQuery API fails."""
