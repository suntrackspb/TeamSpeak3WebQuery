from dataclasses import dataclass
from typing import TypedDict, Optional


class ServerCreateProperties(TypedDict, total=False):
    virtualserver_name: str
    virtualserver_maxclients: int
    virtualserver_port: int
    virtualserver_welcomemessage: Optional[str]
    virtualserver_password: Optional[str]
    virtualserver_codec_encryption_mode: Optional[str]
    virtualserver_encryption_ciphers: Optional[str]
    virtualserver_hostmessage: Optional[str]
    virtualserver_hostmessage_mode: Optional[str]
    virtualserver_default_server_group: Optional[int]
    virtualserver_default_channel_group: Optional[int]
    virtualserver_hostbanner_url: Optional[str]
    virtualserver_hostbanner_gfx_url: Optional[str]
    virtualserver_hostbanner_gfx_interval: Optional[int]
    virtualserver_weblist_enabled: Optional[int]
    virtualserver_machine_id: Optional[str]
    virtualserver_autostart: Optional[int]


class ServerEditProperties(TypedDict, total=False):
    virtualserver_name: str
    virtualserver_maxclients: int
    virtualserver_welcomemessage: Optional[str]
    virtualserver_password: Optional[str]
    virtualserver_codec_encryption_mode: Optional[str]
    virtualserver_encryption_ciphers: Optional[str]
    virtualserver_hostmessage: Optional[str]
    virtualserver_hostmessage_mode: Optional[str]
    virtualserver_default_server_group: Optional[int]
    virtualserver_default_channel_group: Optional[int]
    virtualserver_default_channel_admin_group: Optional[int]
    virtualserver_hostbanner_url: Optional[str]
    virtualserver_hostbanner_gfx_url: Optional[str]
    virtualserver_hostbanner_gfx_interval: Optional[int]
    virtualserver_hostbanner_mode: Optional[int]
    virtualserver_hostbutton_tooltip: Optional[str]
    virtualserver_hostbutton_url: Optional[str]
    virtualserver_hostbutton_gfx_url: Optional[str]
    virtualserver_weblist_enabled: Optional[int]
    virtualserver_reserved_slots: Optional[int]
    virtualserver_name_phonetic: Optional[str]
    virtualserver_icon_id: Optional[int]
    virtualserver_needed_identity_security_level: Optional[int]


@dataclass
class ServerCreateResponse:
    sid: int
    token: str
    virtualserver_port: int

    @staticmethod
    def from_dict(data: dict) -> 'ServerCreateResponse':
        return ServerCreateResponse(
            sid=int(data['sid']),
            token=data['token'],
            virtualserver_port=int(data['virtualserver_port']),
        )
