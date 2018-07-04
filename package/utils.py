def xstr(s):
    # type: (str) -> str
    """
    Converts `s` into a blank string is it is None
    otherwise return `s`
    """
    return '' if s is None else str(s)
