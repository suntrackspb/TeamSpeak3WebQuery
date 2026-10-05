import asyncio
import os

from dotenv import load_dotenv
from ts3_web_query import Client, TeamSpeakAPIError, TeamSpeakConnectionError
from ts3_web_query.constants import TargetMode

load_dotenv()


async def main():
    async with Client(
        api_url=os.getenv("TS3_API_URL"),
        api_key=os.getenv("TS3_API_KEY"),
        instance_id=int(os.getenv("TS3_INSTANCE_ID", "1")),
    ) as client:
        # Сервер
        print(await client.server.version())
        print(await client.server.server_info())

        # Каналы
        for channel in await client.channel.channel_list():
            print(channel.cid, channel.channel_name, channel.total_clients)

        # Клиенты онлайн (query-клиенты тоже в списке: client_type == 1)
        clients = await client.clients.client_list(["uid", "groups"])
        users = [c for c in clients if c.client_type == 0]
        for user in users:
            print(user.clid, user.client_nickname, user.client_servergroups)

        # Сообщение в канал и личное сообщение первому клиенту
        await client.messaging.send_text_message(TargetMode.CHANNEL, "Привет из ts3_web_query!")
        if users:
            await client.messaging.send_private_message(users[0].clid, "Привет!")

        # Пустой результат — это пустой список, а не ошибка
        print(f"банов: {len(await client.messaging.ban_list())}")

        # Ошибки TeamSpeak — исключение TeamSpeakAPIError с кодом и сообщением
        try:
            await client.channel.channel_info(99999)
        except TeamSpeakAPIError as exc:
            print("ошибка сервера:", exc.code, exc.message)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except TeamSpeakConnectionError as exc:
        print("нет связи с WebQuery:", exc)
