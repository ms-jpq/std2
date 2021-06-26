from contextlib import contextmanager
from locale import strcoll
from pathlib import Path, PurePath
from sqlite3 import Cursor, register_adapter, register_converter
from sqlite3.dbapi2 import Connection, Row
from typing import AbstractSet, Iterable, Iterator, Mapping, Union
from unicodedata import normalize
from uuid import UUID

SQL_TYPES = Union[int, float, str, bytes, None]
SQL_PARAM = Mapping[str, SQL_TYPES]
SQL_PARAMS = Iterable[SQL_PARAM]


def escape(nono: AbstractSet[str], escape: str, param: str) -> str:
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
    try:
        yield None
    finally:
        cursor.execute("END TRANSACTION")


def _normalize(text: str) -> str:
    return normalize("NFC", text)


def _lower(text: str) -> str:
    return text.casefold()


def _like_esc(like: str, esc: str) -> str:
    escaped = escape(nono={"%", "_"}, escape=esc, param=like)
    return f"{escaped}%"


def add_functions(conn: Connection) -> None:
    conn.row_factory = Row
    conn.create_collation("X_COLLATION", strcoll)
    conn.create_function("X_NORMALIZE", narg=1, func=_normalize, deterministic=True)
    conn.create_function("X_LOWER", narg=1, func=_lower, deterministic=True)
    conn.create_function("X_LIKE_ESC", narg=2, func=_like_esc, deterministic=True)


def add_conversion() -> None:
    register_adapter(PurePath, str)
    register_converter(PurePath.__qualname__, lambda b: PurePath(b.decode()))
    register_converter(Path.__qualname__, lambda b: Path(b.decode()))

    register_adapter(UUID, lambda u: u.bytes)
    register_converter(UUID.__qualname__, lambda b: UUID(bytes=b))

