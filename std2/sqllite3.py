from contextlib import contextmanager
from sqlite3 import Cursor
from typing import FrozenSet, Iterator, Union

SQL_TYPES = Union[int, float, str, bytes, None]


def escape(nono: FrozenSet[str], escape: str, param: str) -> str:
    escape_chars = nono | {escape}

    def cont() -> Iterator[str]:
        for char in param:
            if char in escape_chars:
                yield escape
            yield char

    return "".join(cont())


@contextmanager
def with_transaction(cursor: Cursor) -> Iterator[None]:
    cursor.execute("BEGIN TRANSACTION")
    yield None
    cursor.execute("END TRANSACTION")
