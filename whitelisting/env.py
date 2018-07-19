import os
import sys


def get(env_var):
    # type: (str) -> str
    """
    Given an environment variable name, will return the value if it exists
    otherwise exit
    """
    if env_var in os.environ:
        return os.environ.get(env_var)
    else:
        print("[ERROR] environment variable %s not set" % env_var)
        sys.exit()
