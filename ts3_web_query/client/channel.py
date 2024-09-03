from typing import List

from . import HttpClient
from ..types import ChannelListInfo, TeamSpeakError


class Channel:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def channel_list(self) -> List[ChannelListInfo] | TeamSpeakError:
        channels = await self.http_client.request('channellist')
        if isinstance(channels, list):
            return [ChannelListInfo.from_dict(channel) for channel in channels]
        else:
            return TeamSpeakError(**channels)
