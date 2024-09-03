from . import HttpClient
from ..types import ServerInfo, ServerList, TeamSpeakError


class Server:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def server_list(self) -> ServerList | TeamSpeakError:
        server_list = await self.http_client.request('serverlist')
        if isinstance(server_list, list):
            return [ServerList.from_dict(server) for server in server_list][0]
        else:
            return TeamSpeakError(**server_list)

    async def server_info(self) -> ServerInfo | TeamSpeakError:
        server_info = await self.http_client.request('serverinfo')
        if isinstance(server_info, list):
            return [ServerInfo.from_dict(server) for server in server_info][0]
        else:
            return TeamSpeakError(**server_info)
