from typing import TypedDict


class ClientEditProperties(TypedDict, total=False):
    """Properties accepted by ``clientedit`` / ``clientdbedit`` / ``clientupdate``."""
    client_nickname: str
    client_description: str
    client_is_talker: int
    client_is_channel_commander: int
    client_is_priority_speaker: int
    client_input_muted: int
    client_output_muted: int
    client_away: int
    client_away_message: str
    client_talk_request: int
    client_talk_request_msg: str
    client_icon_id: int
