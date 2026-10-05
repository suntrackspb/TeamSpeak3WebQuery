from ts3_web_query.utils import build_request


def test_build_request_without_params():
    assert build_request('version') == 'version'


def test_build_request_dict_is_urlencoded():
    assert build_request('clientfind', {'pattern': 'a b&c'}) == 'clientfind?pattern=a+b%26c'


def test_build_request_list_is_joined():
    assert build_request('clientlist', ['-uid', '-away']) == 'clientlist?-uid&-away'

