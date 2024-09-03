import aiohttp


class HttpClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    async def request(self, request_string: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=self.api_url + request_string,
                    headers={'x-api-key': self.api_key}
            ) as response:
                json_data = await response.json()

                if json_data.get("status").get("code") == 0:
                    return json_data.get('body')

                return json_data.get("status")
