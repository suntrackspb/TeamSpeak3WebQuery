from ts3_web_query.types import TeamSpeakError
from ts3_web_query.utils import build_request, status_to_error


def test_build_request_without_params():
    assert build_request('version') == 'version'


def test_build_request_dict_is_urlencoded():
    assert build_request('clientfind', {'pattern': 'a b&c'}) == 'clientfind?pattern=a+b%26c'


def test_build_request_list_is_joined():
    assert build_request('clientlist', ['-uid', '-away']) == 'clientlist?-uid&-away'


def test_status_to_error_success_bodies():
    ok = TeamSpeakError(code=0, message='ok')
    assert status_to_error(None) == ok
    assert status_to_error([]) == ok
    assert status_to_error([{'x': 1}]) == ok


def test_status_to_error_failure():
    err = status_to_error({'code': 1281, 'message': 'database empty result set'})
    assert err == TeamSpeakError(code=1281, message='database empty result set', extra_message=None)
