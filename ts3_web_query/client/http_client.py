import aiohttp
from ..utils import build_request
from ..exceptions import TeamSpeakConnectionError


class HttpClient:
    """
    A simple HTTP client for making requests to a specified API.

    Attributes:
        api_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        instance_id (int): The instance ID for the API request.
    """
    def __init__(self, api_url: str, api_key: str, instance_id: int = 1):
        """
        Initializes the HttpClient with the given API URL, API key, and instance ID.

        Args:
            api_url (str): The base URL of the API.
            api_key (str): The API key for authentication.
            instance_id (int): The instance ID for the API request. Defaults to 1.
        """
        self.api_url = api_url
        self._instance_id = instance_id
        self.api_key = api_key
        self._client_session: aiohttp.ClientSession | None = None

    @property
    def instance_id(self) -> int:
        """
        The instance ID for the API request.

        Returns:
            int: The current instance ID.
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, value: int):
        """
        Sets a new instance ID for the API request.

        Args:
            value (int): The new instance ID. Must be a positive integer.

        Raises:
            ValueError: If the provided instance ID is not a positive integer.
        """
        if isinstance(value, int) and value > 0:
            self._instance_id = value
        else:
            raise ValueError("Instance ID must be a positive integer.")

    def _session(self) -> aiohttp.ClientSession:
        if self._client_session is None or self._client_session.closed:
            self._client_session = aiohttp.ClientSession()
        return self._client_session

    async def close(self):
        """Closes the underlying HTTP session, if one was opened."""
        if self._client_session is not None and not self._client_session.closed:
            await self._client_session.close()

    async def request(self, command: str, params: dict | list | None = None):
        """
        Makes an asynchronous GET request to the API.

        Args:
            command (str): The command or endpoint to append to the API URL.
            params (dict | list | None): The parameters to include in the request.

        Returns:
            dict: The response body if the request is successful, or the
                status dict (``{"code": int, "message": str}``) otherwise.

        Raises:
            TeamSpeakConnectionError: If the HTTP request fails or the response
                is not valid JSON / does not contain a status field.
        """
        query = build_request(command, params)
        try:
            async with self._session().get(
                    url=f'{self.api_url}/{self.instance_id}/{query}',
                    headers={'x-api-key': self.api_key}
            ) as response:
                json_data = await response.json(content_type=None)
        except aiohttp.ClientError as exc:
            raise TeamSpeakConnectionError(str(exc)) from exc

        status = json_data.get("status") if isinstance(json_data, dict) else None
        if not isinstance(status, dict):
            raise TeamSpeakConnectionError(f"Unexpected response format: {json_data!r}")

        if status.get("code") == 0:
            return json_data.get('body')

        return status
