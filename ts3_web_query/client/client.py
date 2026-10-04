from .http_client import HttpClient
from .server import Server
from .channel import Channel
from .channel_group import ChannelGroup
from .server_group import ServerGroup
from .client_management import ClientManagement
from .permission import Permission
from .messaging import Messaging


class Client:
    """
    Entry point of the library: one HTTP session shared by all command groups.

    :param api_url: WebQuery base URL, e.g. ``http://127.0.0.1:10080``.
    :param api_key: WebQuery API key (sent as ``x-api-key``).
    :param instance_id: Virtual server ID (``sid``) the commands are sent to.
    :param timeout: Total timeout of a single request in seconds.
    """

    def __init__(self, api_url: str, api_key: str, instance_id: int = 1, timeout: float = 30.0):
        self.http_client = HttpClient(api_url, api_key, instance_id, timeout)
        self.server = Server(self.http_client)
        self.channel = Channel(self.http_client)
        self.channel_group = ChannelGroup(self.http_client)
        self.server_group = ServerGroup(self.http_client)
        self.clients = ClientManagement(self.http_client)
        self.permission = Permission(self.http_client)
        self.messaging = Messaging(self.http_client)

    async def close(self):
        """Closes the underlying HTTP session."""
        await self.http_client.close()

    async def __aenter__(self) -> 'Client':
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
