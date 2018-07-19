import subprocess


class Git(object):
    """
    Generic git command executor using subprocesses.
    Commands are white space separated.
    Returns the return code of the process

    Usage: git('pull origin master')
    """
    def __new__(cls, commands):
        # type: (str) -> int
        return subprocess.call(["git"] + commands.split())

    @staticmethod
    def hub(commands):
        # type: (str) -> int
        """
        Provides extension methods to the git CLI

        usage: git.hub("pull request")
        """
        return subprocess.call(["hub"] + commands.split())
