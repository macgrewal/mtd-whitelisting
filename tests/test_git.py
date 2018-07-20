from whitelisting.git import Git

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


@patch('subprocess.call')
def test_git_called_with_correct_values(mock_call):
    mock_call.return_value = 999
    assert Git("test 1 2 3") == 999
    mock_call.assert_called_with(['git', 'test', '1', '2', '3'])


@patch('subprocess.call')
def test_hub_called_with_correct_values(mock_call):
    mock_call.return_value = 999
    assert Git.hub("test 1 2 3") == 999
    mock_call.assert_called_with(['hub', 'test', '1', '2', '3'])
