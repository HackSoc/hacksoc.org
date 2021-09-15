
def removeprefix(s : str, prefix : str) -> str:
    if s.startswith(prefix) and len(prefix) > 0:
        return s[len(prefix):]
    else:
        return s

def removesuffix(s : str, suffix: str) -> str:
    if s.endswith(suffix) and len(suffix) > 0:
        return s[:-len(suffix)]
    else:
        return s
