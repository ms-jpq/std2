from __future__ import annotations

from sqlite3 import Cursor, Row
from typing import (
    Any,
    AsyncContextManager,
    AsyncIterable,
    AsyncIterator,
    Optional,
    cast,
)

from ..concurrent.futures import Executor


class ACursor(AsyncContextManager[ACursor], AsyncIterable[Row]):
    def __init__(self, chan: Executor, cursor: Cursor) -> None:
        self._chan = chan
        self._cursor = cursor

    async def __aexit__(self, *_: Any) -> None:
        await self._chan.run(self._cursor.close)

    def __aiter__(self) -> AsyncIterator[Row]:
        async def cont() -> AsyncIterator[Row]:
            while rows := await self._chan.run(self._cursor.fetchmany):
                for row in rows:
                    yield row

        return cont()

    @property
    def lastrowid(self) -> Optional[int]:
        return cast(Optional[int], self._cursor.lastrowid)

    async def fetch_one(self) -> Row:
        return await self._chan.run(self._cursor.fetchone)
