from typing import List

from . import HttpClient
from ..constants import GroupType
from ..types import ChannelGroupList, TeamSpeakError


class ChannelGroup:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def channel_group_list(self) -> List[ChannelGroupList] | TeamSpeakError:
        groups = await self.http_client.request('channelgrouplist')
        if isinstance(groups, list):
            return [ChannelGroupList.from_dict(channel_group) for channel_group in groups if
                    int(channel_group['type']) == GroupType.REGULAR]
        else:
            return TeamSpeakError(**groups)
