from typing import List

from . import HttpClient
from ..constants import GroupType
from ..types import ServerGroupList, TeamSpeakError


class ServerGroup:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def server_groups_list(self) -> List[ServerGroupList] | TeamSpeakError:
        server_groups = await self.http_client.request('servergrouplist')
        if isinstance(server_groups, list):
            return [ServerGroupList.from_dict(server_group) for server_group in server_groups if
                    int(server_group['type']) == GroupType.REGULAR]
        else:
            return TeamSpeakError(**server_groups)

