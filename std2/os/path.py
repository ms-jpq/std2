from os.path import basename, dirname
from typing import Iterator


def ancestors(path: str) -> Iterator[str]:
    parent = dirname(path)
    if not path:
        return
    elif path == parent:
        yield path
    else:
        yield from ancestors(parent)
        yield path


def segments(path: str) -> Iterator[str]:
    parent = dirname(path)
    if not path or path == parent:
        return
    else:
        base = basename(path)
        yield from segments(parent)
        yield base
