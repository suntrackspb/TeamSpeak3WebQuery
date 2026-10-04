from dataclasses import dataclass


@dataclass
class TeamSpeakError:
    code: int
    message: str
    extra_message: str | None = None
