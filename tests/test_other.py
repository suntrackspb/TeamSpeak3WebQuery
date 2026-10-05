import pytest

from ts3_web_query import TeamSpeakAPIError
from ts3_web_query.constants import TargetMode
from ts3_web_query.types.server import ServerVersion

from .conftest import fail, ok


async def test_version(client, server):
    server.reply('version', ok([{'version': '3.13.7', 'platform': 'Linux', 'build': '1655727713'}]))
    assert await client.server.version() == ServerVersion('3.13.7', 'Linux', 1655727713)


async def test_channel_add_perm_posts_objects(client, server):
    server.reply('channeladdperm', ok())
    assert await client.channel.channel_add_perm(2, {10: 5, 11: 6}) is None
    assert server.last.method == 'POST'
    assert server.last.json == [
        {'cid': 2, 'permid': 10, 'permvalue': 5},
        {'cid': 2, 'permid': 11, 'permvalue': 6},
    ]


async def test_channel_list_error_is_raised(client, server):
    server.reply('channellist', fail(2568, 'insufficient client permissions', 'failed_permid=1'))
    with pytest.raises(TeamSpeakAPIError, match='2568 insufficient client permissions .failed_permid=1.'):
        await client.channel.channel_list()


async def test_ban_list_empty_result_is_empty_list(client, server):
    server.reply('banlist', fail(1281, 'database empty result set'))
    assert await client.messaging.ban_list() == []


async def test_ban_add_requires_a_target(client):
    with pytest.raises(ValueError):
        await client.messaging.ban_add()


async def test_send_text_message_private_list_body_is_success(client, server):
    server.reply('sendtextmessage', ok([{'msg': 'hi'}]))
    assert await client.messaging.send_text_message(TargetMode.CLIENT, 'hi', target=3) is None


async def test_client_can_be_closed_manually():
    from ts3_web_query import Client
    c = Client('http://ts3.test:10080', 'k', timeout=5)
    assert c.http_client.timeout == 5
    await c.close()
