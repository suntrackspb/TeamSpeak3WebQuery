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
