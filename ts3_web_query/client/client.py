from .http_client import HttpClient
from .server import Server
from .channel import Channel
from .channel_group import ChannelGroup
from .server_group import ServerGroup


class Client:
    def __init__(self, api_url: str, api_key: str, instance_id: int = 1):
        self.http_client = HttpClient(api_url, api_key, instance_id)
        self.server = Server(self.http_client)
        self.channel = Channel(self.http_client)
        self.channel_group = ChannelGroup(self.http_client)
        self.server_group = ServerGroup(self.http_client)

    async def close(self):
        """Closes the underlying HTTP session."""
        await self.http_client.close()

    async def __aenter__(self) -> 'Client':
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
