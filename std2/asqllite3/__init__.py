from typing import Iterator, Set

from .connection import AConnection
from .cursor import ACursor
from .types import SQL_TYPES


def sql_escape(param: str, nono: Set[str], escape: str) -> str:
    def cont() -> Iterator[str]:
        for char in param:
            if char in nono:
                yield escape
            yield char

    return "".join(cont())
