from dataclasses import dataclass
from typing import Union


@dataclass
class TeamSpeakError:
    code: int
    message: str
    extra_message: Union[str, None]
