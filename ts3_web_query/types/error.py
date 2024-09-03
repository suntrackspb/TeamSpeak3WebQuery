from dataclasses import dataclass


@dataclass
class TeamSpeakError:
    code: int
    message: str
