import asyncio
import os

from dotenv import load_dotenv
from ts3_web_query.client import Client
from ts3_web_query.constants import TargetMode
from ts3_web_query.types import TeamSpeakError

load_dotenv()


async def main():
    async with Client(
        api_url=os.getenv("TS3_API_URL"),
        api_key=os.getenv("TS3_API_KEY"),
    ) as client:
        # Сервер
        print(await client.server.version())
        print(await client.server.server_info())

        # Каналы
        for channel in await client.channel.channel_list():
            print(channel.cid, channel.channel_name, channel.total_clients)

        # Клиенты онлайн (query-клиенты тоже в списке: client_type == 1)
        clients = await client.clients.client_list(["uid", "groups"])
        if isinstance(clients, TeamSpeakError):
            print("ошибка:", clients.message)
            return
        users = [c for c in clients if c.client_type == 0]
        for user in users:
            print(user.clid, user.client_nickname, user.client_servergroups)

        # Сообщение в канал и личное сообщение первому клиенту
        await client.messaging.send_text_message(TargetMode.CHANNEL, "Привет из ts3_web_query!")
        if users:
            await client.messaging.send_private_message(users[0].clid, "Привет!")

        # Ошибки TeamSpeak возвращаются значением, а не исключением.
        # Пустой список банов — это код 1281, а не пустой список.
        bans = await client.messaging.ban_list()
        if isinstance(bans, TeamSpeakError):
            print("баны:", bans.code, bans.message)
        else:
            print(f"банов: {len(bans)}")


if __name__ == "__main__":
    asyncio.run(main())
