from ts3_web_query.constants import ReasonId
from ts3_web_query.types import TeamSpeakError

from .conftest import fail, ok


async def test_client_list_parses_items_and_flags(client, server):
    server.reply('clientlist', ok([
        {'clid': '3', 'cid': '1', 'client_database_id': '7', 'client_nickname': 'bob', 'client_type': '0',
         'client_unique_identifier': 'uid=', 'client_away': '0'},
    ]))
    result = await client.clients.client_list(['uid', 'away'])
    assert len(result) == 1
    assert (result[0].clid, result[0].client_nickname, result[0].client_unique_identifier) == (3, 'bob', 'uid=')
    assert server.last.query == '-uid&-away'


async def test_client_list_empty_body(client, server):
    server.reply('clientlist', ok(None))
    assert await client.clients.client_list() == []


async def test_client_info_error(client, server):
    server.reply('clientinfo', fail(512, 'invalid clientID'))
    assert await client.clients.client_info(99) == TeamSpeakError(512, 'invalid clientID')


async def test_client_move_posts_array_of_clids(client, server):
    server.reply('clientmove', ok())
    result = await client.clients.client_move([3, 4], 2, cpw='pw')
    assert result == TeamSpeakError(0, 'ok')
    assert server.last.method == 'POST'
    assert server.last.json == {'clid': [3, 4], 'cid': 2, 'cpw': 'pw'}


async def test_client_kick_body(client, server):
    server.reply('clientkick', ok())
    await client.clients.client_kick([5], ReasonId.KICK_FROM_SERVER, 'bye')
    assert server.last.method == 'POST'
    assert server.last.json == {'clid': [5], 'reasonid': 5, 'reasonmsg': 'bye'}


async def test_client_add_perm_distinguishes_permid_and_permsid(client, server):
    server.reply('clientaddperm', ok())
    await client.clients.client_add_perm(5, [(12, 1, 0), ('i_client_talk_power', 50, 1)])
    assert server.last.method == 'POST'
    assert server.last.json == [
        {'cldbid': 5, 'permid': 12, 'permvalue': 1, 'permskip': 0},
        {'cldbid': 5, 'permsid': 'i_client_talk_power', 'permvalue': 50, 'permskip': 1},
    ]
