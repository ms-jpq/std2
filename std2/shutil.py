from functools import lru_cache
from itertools import cycle
from os import linesep
from shutil import get_terminal_size
from typing import Any, Iterator
from unicodedata import east_asian_width

_UNICODE_WIDTH_LOOKUP = {
    "W": 2,  # CJK
    "N": 0,  # Non printable
}


def display_width(tabsize: int, string: str) -> int:
    def cont() -> Iterator[int]:
        for char in string:
            if char == "\t":
                yield tabsize
            else:
                code = east_asian_width(char)
                yield _UNICODE_WIDTH_LOOKUP.get(code, 1)

    return sum(cont())


def _cols() -> int:
    cols, _ = get_terminal_size()
    return cols


@lru_cache
def hr(sep: str = "-", tabsize: int = 4, cols: int = _cols()) -> str:
    def cont() -> Iterator[str]:
        source = cycle(zip(sep, (display_width(tabsize, string=char) for char in sep)))
        seen = 0
        for char, length in source:
            seen += length
            if seen < cols:
                yield char
            else:
                break

    line = "".join(cont())
    return line


def hr_print(thing: Any, sep: str = "-", tabsize: int = 4) -> str:
    line = hr(sep=sep, tabsize=tabsize)
    msg = f"{line}{linesep}{thing}{linesep}{line}"
    return msg
