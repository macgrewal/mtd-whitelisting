import subprocess
from whitelisting.cd import cd

try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser


class Config(object):
    """Configuration manager for storing a retrieving credentials"""
    def __init__(self):
        _config = configparser.ConfigParser()
        self._config = _config
        config_file = _config.read("/etc/.creds")
        if len(config_file) == 0:
            print("> /etc/.creds file does not exist")
            input("press ENTER to let me create /etc/.creds, press Ctrl+C to exit")
            print("> creating /etc/.creds file")
            with cd("/etc"):
                subprocess.call(["sudo", "touch", ".creds"])
                subprocess.call(["sudo", "chmod", "777", ".creds"])

    def insert(self, key, value):
        if self._config.has_section("configuration") is False:
            self._config.add_section("configuration")
        
        self._config.set("configuration", key, value)
        with open('/etc/.creds', 'w') as configfile:
            self._config.write(configfile) 

    def get(self, key):
        """
        If the key exists, will return the corresponding value
        else will return None
        """
        if self._config.has_option("configuration", key):
            return self._config.get("configuration", key)
        else:
            return None
