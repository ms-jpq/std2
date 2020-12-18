from __future__ import annotations

from sqlite3 import Cursor, Row
from typing import (
    Any,
    AsyncContextManager,
    AsyncIterable,
    AsyncIterator,
    Iterable,
    Optional,
    Sequence,
    Tuple,
    cast,
)

from ..concurrent.futures import AExecutor
from .types import SQL_TYPES


class ACursor(AsyncContextManager[ACursor], AsyncIterable[Row]):
    def __init__(self, exe: AExecutor, cursor: Cursor) -> None:
        self._exe = exe
        self._cursor = cursor

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    def __aiter__(self) -> AsyncIterator[Row]:
        async def cont() -> AsyncIterator[Row]:
            while rows := await self.fetchmany():
                for row in rows:
                    yield row

        return cont()

    @property
    def rowcount(self) -> int:
        return cast(int, self._cursor.rowcount)

    @property
    def lastrowid(self) -> Optional[int]:
        return cast(Optional[int], self._cursor.lastrowid)

    @property
    def arraysize(self) -> int:
        return cast(int, self._cursor.arraysize)

    @arraysize.setter
    def arraysize(self, n: int) -> None:
        self._cursor.arraysize = n

    @property
    def description(self) -> Sequence[Tuple[Any, None, None, None, None, None, None]]:
        return cast(
            Sequence[Tuple[Any, None, None, None, None, None, None]],
            self._cursor.description,
        )

    async def execute(self, sql: str, params: Iterable[SQL_TYPES]) -> None:
        await self._exe.submit(self._cursor.execute, sql, params)

    async def executemany(
        self, sql: str, params: Iterable[Iterable[SQL_TYPES]]
    ) -> None:
        await self._exe.submit(self._cursor.executemany, sql, params)

    async def executescript(self, sql: str) -> None:
        await self._exe.submit(self._cursor.executescript, sql)

    async def fetchone(self) -> Row:
        return await self._exe.submit(self._cursor.fetchone)

    async def fetchmany(self, size: Optional[int] = None) -> Sequence[Row]:
        fetch_size = self._cursor.arraysize if size is None else size
        return await self._exe.submit(self._cursor.fetchmany, fetch_size)

    async def fetchall(self) -> Sequence[Row]:
        return await self._exe.submit(self._cursor.fetchall)

    async def close(self) -> None:
        await self._exe.submit(self._cursor.close)