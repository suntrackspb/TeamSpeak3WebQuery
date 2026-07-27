from typing import TypedDict, Optional


class ChannelCreateProperties(TypedDict, total=False):
    channel_name: str
    channel_topic: Optional[str]
    channel_description: Optional[str]
    channel_password: Optional[str]
    channel_codec: Optional[int]
    channel_codec_quality: Optional[int]
    channel_maxclients: Optional[int]
    channel_maxfamilyclients: Optional[int]
    channel_order: Optional[int]
    channel_flag_permanent: Optional[int]
    channel_flag_semi_permanent: Optional[int]
    channel_flag_default: Optional[int]
    channel_flag_maxclients_unlimited: Optional[int]
    channel_flag_maxfamilyclients_unlimited: Optional[int]
    channel_flag_maxfamilyclients_inherited: Optional[int]
    channel_needed_talk_power: Optional[int]
    channel_name_phonetic: Optional[str]
    channel_codec_is_unencrypted: Optional[int]
    channel_icon_id: Optional[int]
    cpid: Optional[int]


class ChannelEditProperties(ChannelCreateProperties, total=False):
    pass
