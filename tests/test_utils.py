from whitelisting import utils


def test_xstr_returns_string_with_number():
    assert utils.xstr(1) == '1'


def test_xstr_returns_string_with_string():
    assert utils.xstr('test') == 'test'


def test_xstr_returns_blank_string_with_none():
    assert utils.xstr(None) == ''
