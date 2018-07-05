def xstr(s):
    # type: (any) -> str
    """
    Converts `s` into a blank string if it is None
    otherwise return `s`
    """
    return '' if s is None else str(s)
