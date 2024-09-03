from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class TeamSpeakError:
    code: int
    message: str
    extra_message: Optional[dict] = None
