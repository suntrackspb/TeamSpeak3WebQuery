from dataclasses import dataclass


@dataclass
class ChannelListInfo:
    cid: int
    pid: int
    channel_name: str
    channel_needed_subscribe_power: int
    channel_order: int
    total_clients: int

    @staticmethod
    def from_dict(data: dict) -> 'ChannelListInfo':
        return ChannelListInfo(
            cid=int(data['cid']),
            pid=int(data['pid']),
            channel_name=data['channel_name'],
            channel_needed_subscribe_power=int(data['channel_needed_subscribe_power']),
            channel_order=int(data['channel_order']),
            total_clients=int(data['total_clients'])
        )


@dataclass
class ChannelInfo:
    pid: int
    channel_name: str
    channel_topic: str
    channel_description: str
    channel_password: str
    channel_flag_password: int
    channel_codec: int
    channel_codec_quality: int
    channel_codec_latency_factor: int
    channel_codec_is_unencrypted: int
    channel_maxclients: int
    channel_maxfamilyclients: int
    channel_order: int
    channel_flag_permanent: int
    channel_flag_semi_permanent: int
    channel_flag_default: int
    channel_flag_maxclients_unlimited: int
    channel_flag_maxfamilyclients_unlimited: int
    channel_flag_maxfamilyclients_inherited: int
    channel_needed_talk_power: int
    channel_name_phonetic: str
    channel_filepath: str
    channel_forced_silence: int
    channel_icon_id: int
    channel_security_salt: str
    channel_delete_delay: int
    channel_unique_identifier: str
    seconds_empty: int

    @staticmethod
    def from_dict(data: dict) -> 'ChannelInfo':
        return ChannelInfo(
            pid=int(data.get('pid', 0)),
            channel_name=str(data.get('channel_name', '')),
            channel_topic=str(data.get('channel_topic', '')),
            channel_description=str(data.get('channel_description', '')),
            channel_password=str(data.get('channel_password', '')),
            channel_flag_password=int(data.get('channel_flag_password', 0)),
            channel_codec=int(data.get('channel_codec', 0)),
            channel_codec_quality=int(data.get('channel_codec_quality', 0)),
            channel_codec_latency_factor=int(data.get('channel_codec_latency_factor', 0)),
            channel_codec_is_unencrypted=int(data.get('channel_codec_is_unencrypted', 0)),
            channel_maxclients=int(data.get('channel_maxclients', 0)),
            channel_maxfamilyclients=int(data.get('channel_maxfamilyclients', 0)),
            channel_order=int(data.get('channel_order', 0)),
            channel_flag_permanent=int(data.get('channel_flag_permanent', 0)),
            channel_flag_semi_permanent=int(data.get('channel_flag_semi_permanent', 0)),
            channel_flag_default=int(data.get('channel_flag_default', 0)),
            channel_flag_maxclients_unlimited=int(data.get('channel_flag_maxclients_unlimited', 0)),
            channel_flag_maxfamilyclients_unlimited=int(data.get('channel_flag_maxfamilyclients_unlimited', 0)),
            channel_flag_maxfamilyclients_inherited=int(data.get('channel_flag_maxfamilyclients_inherited', 0)),
            channel_needed_talk_power=int(data.get('channel_needed_talk_power', 0)),
            channel_name_phonetic=str(data.get('channel_name_phonetic', '')),
            channel_filepath=str(data.get('channel_filepath', '')),
            channel_forced_silence=int(data.get('channel_forced_silence', 0)),
            channel_icon_id=int(data.get('channel_icon_id', 0)),
            channel_security_salt=str(data.get('channel_security_salt', '')),
            channel_delete_delay=int(data.get('channel_delete_delay', 0)),
            channel_unique_identifier=str(data.get('channel_unique_identifier', '')),
            seconds_empty=int(data.get('seconds_empty', 0)),
        )


@dataclass
class ChannelFindResult:
    cid: int
    channel_name: str

    @staticmethod
    def from_dict(data: dict) -> 'ChannelFindResult':
        return ChannelFindResult(
            cid=int(data['cid']),
            channel_name=str(data['channel_name']),
        )


@dataclass
class ChannelPermission:
    permid: int
    permvalue: int
    permnegated: int
    permskip: int

    @staticmethod
    def from_dict(data: dict) -> 'ChannelPermission':
        return ChannelPermission(
            permid=int(data.get('permid', 0)),
            permvalue=int(data.get('permvalue', 0)),
            permnegated=int(data.get('permnegated', 0)),
            permskip=int(data.get('permskip', 0)),
        )
