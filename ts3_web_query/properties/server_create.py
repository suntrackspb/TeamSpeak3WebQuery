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


class InstanceEditProperties(TypedDict, total=False):
    """Properties accepted by ``instanceedit`` (server instance settings)."""
    serverinstance_guest_serverquery_group: int
    serverinstance_template_serveradmin_group: int
    serverinstance_template_serverdefault_group: int
    serverinstance_template_channeladmin_group: int
    serverinstance_template_channeldefault_group: int
    serverinstance_filetransfer_port: int
    serverinstance_max_download_total_bandwidth: int
    serverinstance_max_upload_total_bandwidth: int
    serverinstance_serverquery_flood_commands: int
    serverinstance_serverquery_flood_time: int
    serverinstance_serverquery_ban_time: int
    serverinstance_pending_connections_per_ip: int
    serverinstance_serverquery_max_connections_per_ip: int
