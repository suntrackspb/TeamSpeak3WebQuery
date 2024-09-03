from dataclasses import dataclass


@dataclass
class ServerList:
    virtualserver_autostart: int
    virtualserver_clientsonline: int
    virtualserver_id: int
    virtualserver_machine_id: str
    virtualserver_maxclients: int
    virtualserver_name: str
    virtualserver_port: int
    virtualserver_queryclientsonline: int
    virtualserver_status: str
    virtualserver_uptime: int

    @staticmethod
    def from_dict(data: dict) -> 'ServerList':
        return ServerList(
            virtualserver_autostart=int(data['virtualserver_autostart']),
            virtualserver_clientsonline=int(data['virtualserver_clientsonline']),
            virtualserver_id=int(data['virtualserver_id']),
            virtualserver_machine_id=data['virtualserver_machine_id'],
            virtualserver_maxclients=int(data['virtualserver_maxclients']),
            virtualserver_name=data['virtualserver_name'],
            virtualserver_port=int(data['virtualserver_port']),
            virtualserver_queryclientsonline=int(data['virtualserver_queryclientsonline']),
            virtualserver_status=data['virtualserver_status'],
            virtualserver_uptime=int(data['virtualserver_uptime']),
        )


@dataclass
class ServerInfo:
    connection_bandwidth_received_last_minute_total: int
    connection_bandwidth_received_last_second_total: int
    connection_bandwidth_sent_last_minute_total: int
    connection_bandwidth_sent_last_second_total: int
    connection_bytes_received_control: int
    connection_bytes_received_keepalive: int
    connection_bytes_received_speech: int
    connection_bytes_received_total: int
    connection_bytes_sent_control: int
    connection_bytes_sent_keepalive: int
    connection_bytes_sent_speech: int
    connection_bytes_sent_total: int
    connection_filetransfer_bandwidth_received: int
    connection_filetransfer_bandwidth_sent: int
    connection_filetransfer_bytes_received_total: int
    connection_filetransfer_bytes_sent_total: int
    connection_packets_received_control: int
    connection_packets_received_keepalive: int
    connection_packets_received_speech: int
    connection_packets_received_total: int
    connection_packets_sent_control: int
    connection_packets_sent_keepalive: int
    connection_packets_sent_speech: int
    connection_packets_sent_total: int
    virtualserver_antiflood_points_needed_command_block: int
    virtualserver_antiflood_points_needed_ip_block: int
    virtualserver_antiflood_points_needed_plugin_block: int
    virtualserver_antiflood_points_tick_reduce: int
    virtualserver_ask_for_privilegekey: int
    virtualserver_autostart: int
    virtualserver_capability_extensions: str
    virtualserver_channel_temp_delete_delay_default: int
    virtualserver_channelsonline: int
    virtualserver_client_connections: int
    virtualserver_clientsonline: int
    virtualserver_codec_encryption_mode: int
    virtualserver_complain_autoban_count: int
    virtualserver_complain_autoban_time: int
    virtualserver_complain_remove_time: int
    virtualserver_created: int
    virtualserver_default_channel_admin_group: int
    virtualserver_default_channel_group: int
    virtualserver_default_server_group: int
    virtualserver_download_quota: int
    virtualserver_file_storage_class: str
    virtualserver_filebase: str
    virtualserver_flag_password: int
    virtualserver_hostbanner_gfx_interval: int
    virtualserver_hostbanner_gfx_url: str
    virtualserver_hostbanner_mode: int
    virtualserver_hostbanner_url: str
    virtualserver_hostbutton_gfx_url: str
    virtualserver_hostbutton_tooltip: str
    virtualserver_hostbutton_url: str
    virtualserver_hostmessage: str
    virtualserver_hostmessage_mode: int
    virtualserver_icon_id: int
    virtualserver_id: int
    virtualserver_ip: str
    virtualserver_log_channel: int
    virtualserver_log_client: int
    virtualserver_log_filetransfer: int
    virtualserver_log_permissions: int
    virtualserver_log_query: int
    virtualserver_log_server: int
    virtualserver_machine_id: str
    virtualserver_max_download_total_bandwidth: int
    virtualserver_max_upload_total_bandwidth: int
    virtualserver_maxclients: int
    virtualserver_min_android_version: int
    virtualserver_min_client_version: int
    virtualserver_min_clients_in_channel_before_forced_silence: int
    virtualserver_min_ios_version: int
    virtualserver_month_bytes_downloaded: int
    virtualserver_month_bytes_uploaded: int
    virtualserver_name: str
    virtualserver_name_phonetic: str
    virtualserver_needed_identity_security_level: int
    virtualserver_nickname: str
    virtualserver_password: str
    virtualserver_platform: str
    virtualserver_port: int
    virtualserver_priority_speaker_dimm_modificator: float
    virtualserver_query_client_connections: int
    virtualserver_queryclientsonline: int
    virtualserver_reserved_slots: int
    virtualserver_status: str
    virtualserver_total_bytes_downloaded: int
    virtualserver_total_bytes_uploaded: int
    virtualserver_total_packetloss_control: float
    virtualserver_total_packetloss_keepalive: float
    virtualserver_total_packetloss_speech: float
    virtualserver_total_packetloss_total: float
    virtualserver_total_ping: float
    virtualserver_unique_identifier: str
    virtualserver_upload_quota: int
    virtualserver_uptime: int
    virtualserver_version: str
    virtualserver_weblist_enabled: int
    virtualserver_welcomemessage: str

    @staticmethod
    def from_dict(data: dict) -> 'ServerInfo':
        return ServerInfo(
            connection_bandwidth_received_last_minute_total=int(
                data['connection_bandwidth_received_last_minute_total']),
            connection_bandwidth_received_last_second_total=int(
                data['connection_bandwidth_received_last_second_total']),
            connection_bandwidth_sent_last_minute_total=int(data['connection_bandwidth_sent_last_minute_total']),
            connection_bandwidth_sent_last_second_total=int(data['connection_bandwidth_sent_last_second_total']),
            connection_bytes_received_control=int(data['connection_bytes_received_control']),
            connection_bytes_received_keepalive=int(data['connection_bytes_received_keepalive']),
            connection_bytes_received_speech=int(data['connection_bytes_received_speech']),
            connection_bytes_received_total=int(data['connection_bytes_received_total']),
            connection_bytes_sent_control=int(data['connection_bytes_sent_control']),
            connection_bytes_sent_keepalive=int(data['connection_bytes_sent_keepalive']),
            connection_bytes_sent_speech=int(data['connection_bytes_sent_speech']),
            connection_bytes_sent_total=int(data['connection_bytes_sent_total']),
            connection_filetransfer_bandwidth_received=int(data['connection_filetransfer_bandwidth_received']),
            connection_filetransfer_bandwidth_sent=int(data['connection_filetransfer_bandwidth_sent']),
            connection_filetransfer_bytes_received_total=int(data['connection_filetransfer_bytes_received_total']),
            connection_filetransfer_bytes_sent_total=int(data['connection_filetransfer_bytes_sent_total']),
            connection_packets_received_control=int(data['connection_packets_received_control']),
            connection_packets_received_keepalive=int(data['connection_packets_received_keepalive']),
            connection_packets_received_speech=int(data['connection_packets_received_speech']),
            connection_packets_received_total=int(data['connection_packets_received_total']),
            connection_packets_sent_control=int(data['connection_packets_sent_control']),
            connection_packets_sent_keepalive=int(data['connection_packets_sent_keepalive']),
            connection_packets_sent_speech=int(data['connection_packets_sent_speech']),
            connection_packets_sent_total=int(data['connection_packets_sent_total']),
            virtualserver_antiflood_points_needed_command_block=int(
                data['virtualserver_antiflood_points_needed_command_block']),
            virtualserver_antiflood_points_needed_ip_block=int(data['virtualserver_antiflood_points_needed_ip_block']),
            virtualserver_antiflood_points_needed_plugin_block=int(
                data['virtualserver_antiflood_points_needed_plugin_block']),
            virtualserver_antiflood_points_tick_reduce=int(data['virtualserver_antiflood_points_tick_reduce']),
            virtualserver_ask_for_privilegekey=int(data['virtualserver_ask_for_privilegekey']),
            virtualserver_autostart=int(data['virtualserver_autostart']),
            virtualserver_capability_extensions=str(data['virtualserver_capability_extensions']),
            virtualserver_channel_temp_delete_delay_default=int(
                data['virtualserver_channel_temp_delete_delay_default']),
            virtualserver_channelsonline=int(data['virtualserver_channelsonline']),
            virtualserver_client_connections=int(data['virtualserver_client_connections']),
            virtualserver_clientsonline=int(data['virtualserver_clientsonline']),
            virtualserver_codec_encryption_mode=int(data['virtualserver_codec_encryption_mode']),
            virtualserver_complain_autoban_count=int(data['virtualserver_complain_autoban_count']),
            virtualserver_complain_autoban_time=int(data['virtualserver_complain_autoban_time']),
            virtualserver_complain_remove_time=int(data['virtualserver_complain_remove_time']),
            virtualserver_created=int(data['virtualserver_created']),
            virtualserver_default_channel_admin_group=int(data['virtualserver_default_channel_admin_group']),
            virtualserver_default_channel_group=int(data['virtualserver_default_channel_group']),
            virtualserver_default_server_group=int(data['virtualserver_default_server_group']),
            virtualserver_download_quota=int(data['virtualserver_download_quota']),
            virtualserver_file_storage_class=str(data['virtualserver_file_storage_class']),
            virtualserver_filebase=str(data['virtualserver_filebase']),
            virtualserver_flag_password=int(data['virtualserver_flag_password']),
            virtualserver_hostbanner_gfx_interval=int(data['virtualserver_hostbanner_gfx_interval']),
            virtualserver_hostbanner_gfx_url=str(data['virtualserver_hostbanner_gfx_url']),
            virtualserver_hostbanner_mode=int(data['virtualserver_hostbanner_mode']),
            virtualserver_hostbanner_url=str(data['virtualserver_hostbanner_url']),
            virtualserver_hostbutton_gfx_url=str(data['virtualserver_hostbutton_gfx_url']),
            virtualserver_hostbutton_tooltip=str(data['virtualserver_hostbutton_tooltip']),
            virtualserver_hostbutton_url=str(data['virtualserver_hostbutton_url']),
            virtualserver_hostmessage=str(data['virtualserver_hostmessage']),
            virtualserver_hostmessage_mode=int(data['virtualserver_hostmessage_mode']),
            virtualserver_icon_id=int(data['virtualserver_icon_id']),
            virtualserver_id=int(data['virtualserver_id']),
            virtualserver_ip=str(data['virtualserver_ip']),
            virtualserver_log_channel=int(data['virtualserver_log_channel']),
            virtualserver_log_client=int(data['virtualserver_log_client']),
            virtualserver_log_filetransfer=int(data['virtualserver_log_filetransfer']),
            virtualserver_log_permissions=int(data['virtualserver_log_permissions']),
            virtualserver_log_query=int(data['virtualserver_log_query']),
            virtualserver_log_server=int(data['virtualserver_log_server']),
            virtualserver_machine_id=str(data['virtualserver_machine_id']),
            virtualserver_max_download_total_bandwidth=int(data['virtualserver_max_download_total_bandwidth']),
            virtualserver_max_upload_total_bandwidth=int(data['virtualserver_max_upload_total_bandwidth']),
            virtualserver_maxclients=int(data['virtualserver_maxclients']),
            virtualserver_min_android_version=int(data['virtualserver_min_android_version']),
            virtualserver_min_client_version=int(data['virtualserver_min_client_version']),
            virtualserver_min_clients_in_channel_before_forced_silence=int(
                data['virtualserver_min_clients_in_channel_before_forced_silence']),
            virtualserver_min_ios_version=int(data['virtualserver_min_ios_version']),
            virtualserver_month_bytes_downloaded=int(data['virtualserver_month_bytes_downloaded']),
            virtualserver_month_bytes_uploaded=int(data['virtualserver_month_bytes_uploaded']),
            virtualserver_name=str(data['virtualserver_name']),
            virtualserver_name_phonetic=str(data['virtualserver_name_phonetic']),
            virtualserver_needed_identity_security_level=int(data['virtualserver_needed_identity_security_level']),
            virtualserver_nickname=str(data['virtualserver_nickname']),
            virtualserver_password=str(data['virtualserver_password']),
            virtualserver_platform=str(data['virtualserver_platform']),
            virtualserver_port=int(data['virtualserver_port']),
            virtualserver_priority_speaker_dimm_modificator=float(
                data['virtualserver_priority_speaker_dimm_modificator']),
            virtualserver_query_client_connections=int(data['virtualserver_query_client_connections']),
            virtualserver_queryclientsonline=int(data['virtualserver_queryclientsonline']),
            virtualserver_reserved_slots=int(data['virtualserver_reserved_slots']),
            virtualserver_status=str(data['virtualserver_status']),
            virtualserver_total_bytes_downloaded=int(data['virtualserver_total_bytes_downloaded']),
            virtualserver_total_bytes_uploaded=int(data['virtualserver_total_bytes_uploaded']),
            virtualserver_total_packetloss_control=float(data['virtualserver_total_packetloss_control']),
            virtualserver_total_packetloss_keepalive=float(data['virtualserver_total_packetloss_keepalive']),
            virtualserver_total_packetloss_speech=float(data['virtualserver_total_packetloss_speech']),
            virtualserver_total_packetloss_total=float(data['virtualserver_total_packetloss_total']),
            virtualserver_total_ping=float(data['virtualserver_total_ping']),
            virtualserver_unique_identifier=str(data['virtualserver_unique_identifier']),
            virtualserver_upload_quota=int(data['virtualserver_upload_quota']),
            virtualserver_uptime=int(data['virtualserver_uptime']),
            virtualserver_version=str(data['virtualserver_version']),
            virtualserver_weblist_enabled=int(data['virtualserver_weblist_enabled']),
            virtualserver_welcomemessage=str(data['virtualserver_welcomemessage']),
        )
