from whitelisting.config import Config

try:
    from unittest.mock import patch
    import configparser as configparser
except ImportError:
    from mock import patch
    import ConfigParser as configparser


# @patch.object(configparser, "ConfigParser")
# def test_config_init(mock_config_parser):
#     mock_config_parser.return_value.read = ['s']
#     Config()
#     mock_config_parser.read.assert_called_with("")
