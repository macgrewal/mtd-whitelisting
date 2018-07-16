import subprocess


class git:
    """
    Generic git command executor using subprocesses
    Commands are white space separated.

    Usage: git('pull origin master')
    """
    def __new__(self, commands):
        self.output = subprocess.call(["git"] + commands.split())
        return self.output

    @staticmethod
    def hub(commands):
        return subprocess.call(["hub"] + commands.split())
