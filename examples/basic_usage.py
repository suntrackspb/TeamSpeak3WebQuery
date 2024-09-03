import asyncio
import os

from dotenv import load_dotenv
from ts3_web_query.client import Client

load_dotenv()


async def main():
    client = Client(
        api_url=os.getenv("TS3_API_URL"),
        api_key=os.getenv("TS3_API_KEY")
    )

    # Работа с серверами
    print(await client.server.server_list())
    print(await client.server.server_info())


if __name__ == "__main__":
    asyncio.run(main())
