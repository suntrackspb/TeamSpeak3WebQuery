"""Table-driven coverage of every implemented command.

Each case describes the wire format a method must produce (HTTP method, command, query / JSON body)
and how a minimal server reply is parsed. The same table drives the generic error-path test.
"""
import pytest

from ts3_web_query.constants import LogLevel, ReasonId, TargetMode
from ts3_web_query.types import TeamSpeakError
from ts3_web_query.types.server import ServerSnapshot

from .conftest import fail, ok

OK = TeamSpeakError(0, 'ok')
# commands that address the whole instance: sent as /{command}, without a virtual server ID in the path
INSTANCE_LEVEL = {'serverlist', 'serveridgetbyport', 'serverdelete', 'servercreate', 'serverstart', 'serverstop',
                  'serverprocessstop', 'hostinfo', 'instanceinfo', 'instanceedit', 'version', 'gm'}
NO_QUERY = ''


class Case:
    def __init__(self, name, call, command, *, method='GET', query=NO_QUERY, json=None, body=None, check=None):
        self.name, self.call, self.command = name, call, command
        self.method, self.query, self.json, self.body, self.check = method, query, json, body, check

    def __repr__(self):
        return self.name


def case(*args, **kwargs):
    return pytest.param(Case(*args, **kwargs), id=args[0])


# --- server --------------------------------------------------------------------------------------------------------
SERVER = [
    case('server_list', lambda c: c.server.server_list(), 'serverlist', body=[]),
    case('server_list_all_offline', lambda c: c.server.server_list(True, True), 'serverlist',
         query='-all&-onlyoffline', body=[]),
    case('server_info', lambda c: c.server.server_info(), 'serverinfo', body=[{'virtualserver_name': 'S'}]),
    case('server_id_get_by_port', lambda c: c.server.server_id_get_by_port(9987), 'serveridgetbyport',
         query='virtualserver_port=9987', body=[{'server_id': '1'}], check=lambda r: r == 1),
    case('server_delete', lambda c: c.server.server_delete(2), 'serverdelete', query='sid=2', check=lambda r: r == OK),
    case('server_create', lambda c: c.server.server_create({'virtualserver_name': 'New'}), 'servercreate',
         query='virtualserver_name=New', body=[{'sid': '2', 'virtualserver_port': '9988', 'token': 't'}]),
    case('server_start', lambda c: c.server.server_start(2), 'serverstart', query='sid=2', check=lambda r: r == OK),
    case('server_stop', lambda c: c.server.server_stop(2), 'serverstop', query='sid=2', check=lambda r: r == OK),
    case('server_process_stop', lambda c: c.server.server_process_stop(), 'serverprocessstop',
         check=lambda r: r == OK),
    case('server_request_connection_info', lambda c: c.server.server_request_connection_info(),
         'serverrequestconnectioninfo', body=[{'connection_ping': '1'}]),
    case('server_edit', lambda c: c.server.server_edit({'virtualserver_name': 'X'}), 'serveredit',
         query='virtualserver_name=X', check=lambda r: r == OK),
    case('server_temp_password_add', lambda c: c.server.server_temp_password_add('pw', 'd', 60), 'servertemppasswordadd',
         query='pw=pw&desc=d&duration=60&tcid=0&tcpw=', check=lambda r: r == OK),
    case('server_temp_password_del', lambda c: c.server.server_temp_password_del('pw'), 'servertemppassworddel',
         query='pw=pw', check=lambda r: r == OK),
    case('server_temp_password_list', lambda c: c.server.server_temp_password_list(), 'servertemppasswordlist',
         body=[]),
    case('host_info', lambda c: c.server.host_info(), 'hostinfo', body=[{'instance_uptime': '1'}]),
    case('whoami', lambda c: c.server.whoami(), 'whoami', body=[{'virtualserver_id': '1'}]),
    case('instance_info', lambda c: c.server.instance_info(), 'instanceinfo', body=[{'serverinstance_database_version': '26'}]),
    case('instance_edit', lambda c: c.server.instance_edit({'serverinstance_serverquery_flood_commands': 50}),
         'instanceedit', query='serverinstance_serverquery_flood_commands=50', check=lambda r: r == OK),
    case('log_view_defaults', lambda c: c.server.log_view(), 'logview', body=[{'last_pos': '1', 'file_size': '2'}]),
    case('log_view_args', lambda c: c.server.log_view(lines=5, reverse=True, instance=False, begin_pos=3), 'logview',
         query='lines=5&reverse=1&instance=0&begin_pos=3', body=[{'last_pos': '1', 'file_size': '2'}]),
    case('log_add', lambda c: c.server.log_add(LogLevel.INFO, 'hello'), 'logadd', query='loglevel=4&logmsg=hello',
         check=lambda r: r == OK),
    case('global_message', lambda c: c.server.global_message('hi'), 'gm', query='msg=hi', check=lambda r: r == OK),
    case('server_snapshot_create', lambda c: c.server.server_snapshot_create(), 'serversnapshotcreate',
         body=[{'version': '3', 'data': 'abc'}]),
    case('server_snapshot_deploy', lambda c: c.server.server_snapshot_deploy(ServerSnapshot(version='3', data='abc')),
         'serversnapshotdeploy', method='POST', json={'data': 'abc', 'version': '3'}, check=lambda r: r == []),
    case('server_snapshot_deploy_mapping',
         lambda c: c.server.server_snapshot_deploy(ServerSnapshot(version='3', data='abc'), mapping=True),
         'serversnapshotdeploy', method='POST', query='-mapping', json={'data': 'abc', 'version': '3'},
         body=[{'cid': '1'}], check=lambda r: r == [{'cid': '1'}]),
    case('version', lambda c: c.server.version(), 'version',
         body=[{'version': '3.13.7', 'platform': 'Linux', 'build': '1'}]),
]

# --- channel -------------------------------------------------------------------------------------------------------
CHANNEL = [
    case('channel_list', lambda c: c.channel.channel_list(), 'channellist',
         body=[{'cid': '1', 'pid': '0', 'channel_name': 'x', 'channel_needed_subscribe_power': '0',
                'channel_order': '0', 'total_clients': '0'}]),
    case('channel_info', lambda c: c.channel.channel_info(1), 'channelinfo', query='cid=1',
         body=[{'channel_name': 'x'}]),
    case('channel_find', lambda c: c.channel.channel_find('lob'), 'channelfind', query='pattern=lob',
         body=[{'cid': '1', 'channel_name': 'lobby'}]),
    case('channel_move', lambda c: c.channel.channel_move(2, 1), 'channelmove', query='cid=2&cpid=1&order=0',
         check=lambda r: r == OK),
    case('channel_create', lambda c: c.channel.channel_create({'channel_name': 'n'}), 'channelcreate',
         query='channel_name=n', body=[{'cid': '7'}], check=lambda r: r == 7),
    case('channel_delete', lambda c: c.channel.channel_delete(2, force=True), 'channeldelete', query='cid=2&force=1',
         check=lambda r: r == OK),
    case('channel_edit', lambda c: c.channel.channel_edit(2, {'channel_name': 'z'}), 'channeledit',
         query='cid=2&channel_name=z', check=lambda r: r == OK),
    case('channel_perm_list', lambda c: c.channel.channel_perm_list(2), 'channelpermlist', query='cid=2',
         body=[{'permid': '1', 'permvalue': '5'}]),
    case('channel_perm_list_permsid', lambda c: c.channel.channel_perm_list(2, permsid=True), 'channelpermlist',
         query='cid=2&-permsid', body=[{'permsid': 'x', 'permvalue': '5'}]),
    case('channel_add_perm', lambda c: c.channel.channel_add_perm(2, {10: 5}), 'channeladdperm', method='POST',
         json=[{'cid': 2, 'permid': 10, 'permvalue': 5}], check=lambda r: r == OK),
    case('channel_del_perm', lambda c: c.channel.channel_del_perm(2, [10, 11]), 'channeldelperm', method='POST',
         json=[{'cid': 2, 'permid': 10}, {'cid': 2, 'permid': 11}], check=lambda r: r == OK),
    case('channel_client_perm_list', lambda c: c.channel.channel_client_perm_list(2, 5, permsid=True),
         'channelclientpermlist', query='cid=2&cldbid=5&-permsid', body=[{'permsid': 'x', 'permvalue': '1'}]),
    case('channel_client_add_perm', lambda c: c.channel.channel_client_add_perm(2, 5, [(10, 1), ('p', 2)]),
         'channelclientaddperm', method='POST', check=lambda r: r == OK,
         json=[{'cid': 2, 'cldbid': 5, 'permid': 10, 'permvalue': 1},
               {'cid': 2, 'cldbid': 5, 'permsid': 'p', 'permvalue': 2}]),
    case('channel_client_del_perm', lambda c: c.channel.channel_client_del_perm(2, 5, [10, 'p']),
         'channelclientdelperm', method='POST', check=lambda r: r == OK,
         json=[{'cid': 2, 'cldbid': 5, 'permid': 10}, {'cid': 2, 'cldbid': 5, 'permsid': 'p'}]),
]

# --- channel groups ------------------------------------------------------------------------------------------------
CHANNEL_GROUP = [
    case('channel_group_list', lambda c: c.channel_group.channel_group_list(), 'channelgrouplist',
         body=[{'cgid': '1', 'name': 'Guest', 'type': '1', 'iconid': '0', 'n_member_addp': '0', 'n_member_removep': '0', 'n_modifyp': '0', 'namemode': '0', 'savedb': '1', 'sortid': '0'},
               {'cgid': '2', 'name': 'tpl', 'type': '0', 'iconid': '0', 'n_member_addp': '0', 'n_member_removep': '0', 'n_modifyp': '0', 'namemode': '0', 'savedb': '1', 'sortid': '0'}],
         check=lambda r: [g.cgid for g in r] == [1]),
    case('channel_group_add', lambda c: c.channel_group.channel_group_add('g'), 'channelgroupadd',
         query='name=g&type=1', body=[{'cgid': '9'}], check=lambda r: r == 9),
    case('channel_group_del', lambda c: c.channel_group.channel_group_del(9, True), 'channelgroupdel',
         query='cgid=9&force=1', check=lambda r: r == OK),
    case('channel_group_copy', lambda c: c.channel_group.channel_group_copy(5, 'cp'), 'channelgroupcopy',
         query='scgid=5&tcgid=0&name=cp&type=1', body=[{'cgid': '10'}], check=lambda r: r == 10),
    case('channel_group_rename', lambda c: c.channel_group.channel_group_rename(5, 'n'), 'channelgrouprename',
         query='cgid=5&name=n', check=lambda r: r == OK),
    case('channel_group_perm_list', lambda c: c.channel_group.channel_group_perm_list(5, permsid=True),
         'channelgrouppermlist', query='cgid=5&-permsid', body=[{'permsid': 'x', 'permvalue': '1'}]),
    case('channel_group_add_perm', lambda c: c.channel_group.channel_group_add_perm(5, {1: 2}), 'channelgroupaddperm',
         method='POST', json=[{'cgid': 5, 'permid': 1, 'permvalue': 2}], check=lambda r: r == OK),
    case('channel_group_del_perm', lambda c: c.channel_group.channel_group_del_perm(5, [1]), 'channelgroupdelperm',
         method='POST', json=[{'cgid': 5, 'permid': 1}], check=lambda r: r == OK),
    case('channel_group_client_list', lambda c: c.channel_group.channel_group_client_list(cid=1, cgid=2),
         'channelgroupclientlist', query='cid=1&cgid=2', body=[{'cid': '1', 'cldbid': '3', 'cgid': '2'}]),
    case('set_client_channel_group', lambda c: c.channel_group.set_client_channel_group(5, 1, 3),
         'setclientchannelgroup', query='cgid=5&cid=1&cldbid=3', check=lambda r: r == OK),
]

# --- server groups -------------------------------------------------------------------------------------------------
SERVER_GROUP = [
    case('server_groups_list', lambda c: c.server_group.server_groups_list(), 'servergrouplist',
         body=[{'sgid': '6', 'name': 'Admin', 'type': '1', 'iconid': '0', 'n_member_addp': '0', 'n_member_removep': '0', 'n_modifyp': '0', 'namemode': '0', 'savedb': '1', 'sortid': '0'},
               {'sgid': '1', 'name': 'tpl', 'type': '0', 'iconid': '0', 'n_member_addp': '0', 'n_member_removep': '0', 'n_modifyp': '0', 'namemode': '0', 'savedb': '1', 'sortid': '0'}],
         check=lambda r: [g.sgid for g in r] == [6]),
    case('server_group_add', lambda c: c.server_group.server_group_add('g'), 'servergroupadd', query='name=g&type=1',
         body=[{'sgid': '9'}], check=lambda r: r == 9),
    case('server_group_del', lambda c: c.server_group.server_group_del(9), 'servergroupdel', query='sgid=9&force=0',
         check=lambda r: r == OK),
    case('server_group_copy', lambda c: c.server_group.server_group_copy(5, 'cp'), 'servergroupcopy',
         query='ssgid=5&tsgid=0&name=cp&type=1', body=[{'sgid': '10'}], check=lambda r: r == 10),
    case('server_group_rename', lambda c: c.server_group.server_group_rename(5, 'n'), 'servergrouprename',
         query='sgid=5&name=n', check=lambda r: r == OK),
    case('server_group_perm_list', lambda c: c.server_group.server_group_perm_list(5, permsid=True),
         'servergrouppermlist', query='sgid=5&-permsid', body=[{'permsid': 'x', 'permvalue': '1'}]),
    case('server_group_add_perm', lambda c: c.server_group.server_group_add_perm(5, {1: 2}), 'servergroupaddperm',
         method='POST', check=lambda r: r == OK,
         json=[{'sgid': 5, 'permid': 1, 'permvalue': 2, 'permnegated': 0, 'permskip': 0}]),
    case('server_group_del_perm', lambda c: c.server_group.server_group_del_perm(5, [1]), 'servergroupdelperm',
         method='POST', json=[{'sgid': 5, 'permid': 1}], check=lambda r: r == OK),
    case('server_group_add_client', lambda c: c.server_group.server_group_add_client(5, 3), 'servergroupaddclient',
         query='sgid=5&cldbid=3', check=lambda r: r == OK),
    case('server_group_del_client', lambda c: c.server_group.server_group_del_client(5, 3), 'servergroupdelclient',
         query='sgid=5&cldbid=3', check=lambda r: r == OK),
    case('server_group_client_list', lambda c: c.server_group.server_group_client_list(5, names=True),
         'servergroupclientlist', query='sgid=5&-names', body=[{'cldbid': '3'}]),
    case('server_groups_by_client_id', lambda c: c.server_group.server_groups_by_client_id(3), 'servergroupsbyclientid',
         query='cldbid=3', body=[{'name': 'Admin', 'sgid': '6', 'cldbid': '3'}]),
    case('server_group_auto_add_perm', lambda c: c.server_group.server_group_auto_add_perm(10, {1: 2}),
         'servergroupautoaddperm', method='POST', check=lambda r: r == OK,
         json=[{'sgtype': 10, 'permid': 1, 'permvalue': 2, 'permnegated': 0, 'permskip': 0}]),
    case('server_group_auto_del_perm', lambda c: c.server_group.server_group_auto_del_perm(10, [1]),
         'servergroupautodelperm', method='POST', json=[{'sgtype': 10, 'permid': 1}], check=lambda r: r == OK),
]

# --- clients -------------------------------------------------------------------------------------------------------
CLIENTS = [
    case('client_list', lambda c: c.clients.client_list(['uid', 'away']), 'clientlist', query='-uid&-away',
         body=[{'clid': '3', 'cid': '1', 'client_database_id': '7', 'client_nickname': 'b', 'client_type': '0'}],
         check=lambda r: r[0].clid == 3),
    case('client_info', lambda c: c.clients.client_info(3), 'clientinfo', query='clid=3',
         body=[{'client_nickname': 'b', 'client_servergroups': '6,7'}], check=lambda r: r.client_servergroups == [6, 7]),
    case('client_find', lambda c: c.clients.client_find('b'), 'clientfind', query='pattern=b',
         body=[{'clid': '3', 'client_nickname': 'bob'}]),
    case('client_edit', lambda c: c.clients.client_edit(3, {'client_description': 'd'}), 'clientedit',
         query='clid=3&client_description=d', check=lambda r: r == OK),
    case('client_update', lambda c: c.clients.client_update({'client_nickname': 'n'}), 'clientupdate',
         query='client_nickname=n', check=lambda r: r == OK),
    case('client_move', lambda c: c.clients.client_move([3, 4], 2), 'clientmove', method='POST',
         json={'clid': [3, 4], 'cid': 2}, check=lambda r: r == OK),
    case('client_kick', lambda c: c.clients.client_kick([3], ReasonId.KICK_FROM_CHANNEL), 'clientkick', method='POST',
         json={'clid': [3], 'reasonid': 4}, check=lambda r: r == OK),
    case('client_poke', lambda c: c.clients.client_poke(3, 'hey'), 'clientpoke', query='clid=3&msg=hey',
         check=lambda r: r == OK),
    case('client_db_list', lambda c: c.clients.client_db_list(0, 10), 'clientdblist', query='start=0&duration=10',
         body=[{'cldbid': '7', 'client_nickname': 'b'}]),
    case('client_db_info', lambda c: c.clients.client_db_info(7), 'clientdbinfo', query='cldbid=7',
         body=[{'client_nickname': 'b'}]),
    case('client_db_find', lambda c: c.clients.client_db_find('b'), 'clientdbfind', query='pattern=b',
         body=[{'cldbid': '7'}], check=lambda r: r[0].cldbid == 7),
    case('client_db_find_uid', lambda c: c.clients.client_db_find('x=', by_uid=True), 'clientdbfind',
         query='pattern=x%3D&-uid', body=[{'cldbid': '7'}]),
    case('client_db_edit', lambda c: c.clients.client_db_edit(7, {'client_description': 'd'}), 'clientdbedit',
         query='cldbid=7&client_description=d', check=lambda r: r == OK),
    case('client_db_delete', lambda c: c.clients.client_db_delete(7), 'clientdbdelete', query='cldbid=7',
         check=lambda r: r == OK),
    case('client_get_ids', lambda c: c.clients.client_get_ids('uid='), 'clientgetids', query='cluid=uid%3D',
         body=[{'clid': '3', 'cluid': 'uid=', 'name': 'b'}], check=lambda r: r[0].clid == 3),
    case('client_get_dbid_from_uid', lambda c: c.clients.client_get_dbid_from_uid('uid='), 'clientgetdbidfromuid',
         query='cluid=uid%3D', body=[{'cluid': 'uid=', 'cldbid': '7'}], check=lambda r: r == 7),
    case('client_get_name_from_uid', lambda c: c.clients.client_get_name_from_uid('uid='), 'clientgetnamefromuid',
         query='cluid=uid%3D', body=[{'cluid': 'uid=', 'cldbid': '7', 'name': 'b'}], check=lambda r: r.name == 'b'),
    case('client_get_uid_from_clid', lambda c: c.clients.client_get_uid_from_clid(3), 'clientgetuidfromclid',
         query='clid=3', body=[{'clid': '3', 'cluid': 'uid=', 'nickname': 'b'}], check=lambda r: r.cluid == 'uid='),
    case('client_get_name_from_dbid', lambda c: c.clients.client_get_name_from_dbid(7), 'clientgetnamefromdbid',
         query='cldbid=7', body=[{'cluid': 'uid=', 'cldbid': '7', 'name': 'b'}], check=lambda r: r.cldbid == 7),
    case('client_set_serverquery_login', lambda c: c.clients.client_set_serverquery_login('bot'),
         'clientsetserverquerylogin', query='client_login_name=bot',
         body=[{'client_login_name': 'bot', 'client_login_password': 'pw'}], check=lambda r: r == 'pw'),
    case('client_perm_list', lambda c: c.clients.client_perm_list(7, permsid=True), 'clientpermlist',
         query='cldbid=7&-permsid', body=[{'permsid': 'x', 'permvalue': '1'}]),
    case('client_add_perm', lambda c: c.clients.client_add_perm(7, [(1, 2, 0), ('p', 3, 1)]), 'clientaddperm',
         method='POST', check=lambda r: r == OK,
         json=[{'cldbid': 7, 'permid': 1, 'permvalue': 2, 'permskip': 0},
               {'cldbid': 7, 'permsid': 'p', 'permvalue': 3, 'permskip': 1}]),
    case('client_del_perm', lambda c: c.clients.client_del_perm(7, [1, 'p']), 'clientdelperm', method='POST',
         json=[{'cldbid': 7, 'permid': 1}, {'cldbid': 7, 'permsid': 'p'}], check=lambda r: r == OK),
]

# --- permissions ---------------------------------------------------------------------------------------------------
PERMISSION = [
    case('permission_list', lambda c: c.permission.permission_list(), 'permissionlist',
         body=[{'permid': '1', 'permname': 'x', 'permdesc': 'd'}]),
    case('perm_id_get_by_name', lambda c: c.permission.perm_id_get_by_name(['a', 'b']), 'permidgetbyname',
         method='POST', json=[{'permsid': 'a'}, {'permsid': 'b'}], body=[{'permsid': 'a', 'permid': '1'}]),
    case('perm_overview', lambda c: c.permission.perm_overview(1, 7), 'permoverview', method='POST',
         json=[{'cid': 1, 'cldbid': 7, 'permid': 0}], body=[{'t': '0', 'id1': '1', 'p': '1', 'v': '1'}]),
    case('perm_overview_names', lambda c: c.permission.perm_overview(1, 7, ['a', 3]), 'permoverview', method='POST',
         json=[{'cid': 1, 'cldbid': 7, 'permsid': 'a'}, {'cid': 1, 'cldbid': 7, 'permid': 3}],
         body=[{'t': '0', 'id1': '1', 'p': '1', 'v': '1'}]),
    case('perm_get', lambda c: c.permission.perm_get(['a', 3]), 'permget', method='POST',
         json=[{'permsid': 'a'}, {'permid': 3}], body=[{'permsid': 'a', 'permvalue': '1'}]),
    case('perm_find', lambda c: c.permission.perm_find([3]), 'permfind', method='POST', json=[{'permid': 3}],
         body=[{'t': '0', 'id1': '1', 'p': '3'}]),
    case('perm_reset', lambda c: c.permission.perm_reset(), 'permreset', body=[{'token': 'tok'}],
         check=lambda r: r == 'tok'),
    case('privilege_key_list', lambda c: c.permission.privilege_key_list(), 'privilegekeylist',
         body=[{'token': 't', 'token_type': '0', 'token_id1': '6', 'token_id2': '0', 'token_description': ''}]),
    case('privilege_key_add', lambda c: c.permission.privilege_key_add(0, 6, tokendescription='d'), 'privilegekeyadd',
         query='tokentype=0&tokenid1=6&tokenid2=0&tokendescription=d', body=[{'token': 'tok'}],
         check=lambda r: r == 'tok'),
    case('privilege_key_delete', lambda c: c.permission.privilege_key_delete('tok'), 'privilegekeydelete',
         query='token=tok', check=lambda r: r == OK),
    case('privilege_key_use', lambda c: c.permission.privilege_key_use('tok'), 'privilegekeyuse', query='token=tok',
         check=lambda r: r == OK),
    case('custom_search', lambda c: c.permission.custom_search('k', '%v%'), 'customsearch', query='ident=k&pattern=%v%',
         body=[{'cldbid': '7', 'ident': 'k', 'value': 'v'}]),
    case('custom_info', lambda c: c.permission.custom_info(7), 'custominfo', query='cldbid=7',
         body=[{'cldbid': '7', 'ident': 'k', 'value': 'v'}]),
]

# --- messaging -----------------------------------------------------------------------------------------------------
MESSAGING = [
    case('send_text_message', lambda c: c.messaging.send_text_message(TargetMode.CHANNEL, 'hi'), 'sendtextmessage',
         query='targetmode=2&target=1&msg=hi', check=lambda r: r == OK),
    case('send_private_message', lambda c: c.messaging.send_private_message(3, 'hi'), 'sendtextmessage',
         query='targetmode=1&target=3&msg=hi', body=[{'msg': 'hi'}], check=lambda r: r == OK),
    case('message_list', lambda c: c.messaging.message_list(), 'messagelist',
         body=[{'msgid': '1', 'cluid': 'u=', 'subject': 's', 'flag_read': '0', 'timestamp': '1'}]),
    case('message_add', lambda c: c.messaging.message_add('u=', 's', 'm'), 'messageadd',
         query='cluid=u%3D&subject=s&message=m', check=lambda r: r == OK),
    case('message_del', lambda c: c.messaging.message_del(1), 'messagedel', query='msgid=1', check=lambda r: r == OK),
    case('message_get', lambda c: c.messaging.message_get(1), 'messageget', query='msgid=1',
         body=[{'msgid': '1', 'cluid': 'u=', 'subject': 's', 'message': 'm', 'timestamp': '1'}]),
    case('message_update_flag', lambda c: c.messaging.message_update_flag(1, read=False), 'messageupdateflag',
         query='msgid=1&flag=0', check=lambda r: r == OK),
    case('complain_list', lambda c: c.messaging.complain_list(), 'complainlist', body=[{'tcldbid': '7'}]),
    case('complain_list_for_client', lambda c: c.messaging.complain_list(7), 'complainlist', query='tcldbid=7',
         body=[{'tcldbid': '7'}]),
    case('complain_add', lambda c: c.messaging.complain_add(7, 'm'), 'complainadd', query='tcldbid=7&message=m',
         check=lambda r: r == OK),
    case('complain_del_all', lambda c: c.messaging.complain_del_all(7), 'complaindelall', query='tcldbid=7',
         check=lambda r: r == OK),
    case('complain_del', lambda c: c.messaging.complain_del(7, 8), 'complaindel', query='tcldbid=7&fcldbid=8',
         check=lambda r: r == OK),
    case('ban_client', lambda c: c.messaging.ban_client([3], time=60, banreason='r'), 'banclient', method='POST',
         json={'clid': [3], 'time': 60, 'banreason': 'r'}, body=[{'banid': '4'}, {'banid': '5'}],
         check=lambda r: r == [4, 5]),
    case('ban_list', lambda c: c.messaging.ban_list(), 'banlist', body=[{'banid': '4'}]),
    case('ban_add', lambda c: c.messaging.ban_add(ip='1.2.3.4', time=10), 'banadd', query='ip=1.2.3.4&time=10',
         body=[{'banid': '9'}], check=lambda r: r == 9),
    case('ban_del', lambda c: c.messaging.ban_del(4), 'bandel', query='banid=4', check=lambda r: r == OK),
    case('ban_del_all', lambda c: c.messaging.ban_del_all(), 'bandelall', check=lambda r: r == OK),
]

ALL = SERVER + CHANNEL + CHANNEL_GROUP + SERVER_GROUP + CLIENTS + PERMISSION + MESSAGING


@pytest.mark.parametrize('c', ALL)
async def test_request_and_parsing(c, client, server):
    server.reply(c.command, ok(c.body))
    result = await c.call(client)

    assert not isinstance(result, TeamSpeakError) or result == OK, result
    req = server.last
    assert (req.method, req.command, req.sid) == (c.method, c.command, '' if c.command in INSTANCE_LEVEL else '1')
    assert req.query == c.query
    assert req.json == c.json
    assert req.headers['x-api-key'] == 'secret-key'
    if c.check:
        assert c.check(result), result


@pytest.mark.parametrize('c', ALL)
async def test_server_error_is_returned(c, client, server):
    server.reply(c.command, fail(2568, 'insufficient client permissions', 'failed_permid=1'))
    result = await c.call(client)
    assert result == TeamSpeakError(2568, 'insufficient client permissions', 'failed_permid=1')



@pytest.mark.parametrize('c', ALL)
async def test_list_commands_map_null_body_to_empty_list(c, client, server):
    """The server answers some list commands with a ``null`` body (e.g. ``serverlist -onlyoffline``)."""
    server.reply(c.command, ok(c.body))
    if not isinstance(await c.call(client), list):
        pytest.skip('not a list-returning command')
    server.reply(c.command, ok(None))
    assert await c.call(client) == []
