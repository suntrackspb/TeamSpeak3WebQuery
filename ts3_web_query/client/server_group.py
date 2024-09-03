from typing import List

from . import HttpClient
from ..types import ServerGroupList, TeamSpeakError


class ServerGroup:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def server_groups_list(self) -> List[ServerGroupList] | TeamSpeakError:
        server_groups = await self.http_client.request(f'servergrouplist')
        if isinstance(server_groups, list):
            return [ServerGroupList.from_dict(server_group) for server_group in server_groups if
                    server_group['type'] == "1"]
        else:
            return TeamSpeakError(**server_groups)

