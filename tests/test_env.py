from whitelisting import env

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


@patch.dict("os.environ", {'test_env_var': 'test_value'})
def test_get_returns_the_correct_value():
    assert env.get('test_env_var') == 'test_value'


@patch.dict("os.environ", {'test_env_var': 'test_value'})
def test_get_environ_does_not_contain_key():
    try:
        env.get('to_fail')
    except SystemExit:
        pass
