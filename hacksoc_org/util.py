"""Miscellaneous helper functions"""

def removeprefix(s : str, prefix : str) -> str:
    """Re-implementation of Python 3.9's str.removeprefix
    https://docs.python.org/3/library/stdtypes.html#str.removeprefix

    Args:
        s (str): The string from which to remove the prefix
        prefix (str): prefix to remove

    Returns:
        str: copy of `s`, with `prefix` removed if `s` starts with `prefix`
    """
    if s.startswith(prefix) and len(prefix) > 0:
        return s[len(prefix):]
    else:
        return s

def removesuffix(s : str, suffix: str) -> str:
    """Re-implementation of Python 3.9's str.removesuffix
    https://docs.python.org/3/library/stdtypes.html#str.removesuffix

    Args:
        s (str): The string from which to remove the suffix
        suffix (str): suffix to remove

    Returns:
        str: copy of `s`, with `suffix` removed if `s` ends with `suffix`
    """
    if s.endswith(suffix) and len(suffix) > 0:
        return s[:-len(suffix)]
    else:
        return s
