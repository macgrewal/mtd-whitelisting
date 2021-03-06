from whitelisting import whitelist

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


@patch('requests.get')
def test_http_get_200(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b'test-body'

    assert whitelist.http_get("test-url") == 'test-body'


@patch('requests.get')
def test_http_get_401(mock_get):
    mock_get.return_value.status_code = 401

    try:
        whitelist.http_get("test-url")
    except SystemExit:
        pass


@patch('requests.get')
def test_http_get_unknown_status_code(mock_get):
    mock_get.return_value.status_code = 999

    try:
        whitelist.http_get("test-url")
    except SystemExit:
        pass


def test_get_next_config_id():
    test_config = {
        'Prod.feature-switch.white-list.applicationIds.1': 'test',
        'Prod.feature-switch.white-list.applicationIds.2': 'test',
        'Prod.feature-switch.white-list.applicationIds.3': 'test'
    }
    assert whitelist.get_next_config_id(test_config) == '4'


def test_get_next_config_id_empty_list():
    test_config = {}
    assert whitelist.get_next_config_id(test_config) == '0'
