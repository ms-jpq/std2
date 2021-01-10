from __future__ import annotations

from sqlite3 import Connection, Cursor, Row, connect
from typing import Any, AsyncContextManager, Callable, ContextManager, TypeVar

from .concurrent.aexecutor import AExecutor

T = TypeVar("T")


class AConnection(ContextManager["AConnection"], AsyncContextManager["AConnection"]):
    def __init__(self, database: str = ":memory:") -> None:
        self._aexe = AExecutor(daemon=False)

        def cont() -> Connection:
            conn = connect(database, isolation_level=None)
            conn.row_factory = Row
            return conn

        self._conn = self._aexe.submit(cont)

    def __exit__(self, *_: Any) -> None:
        self.close()

    async def __aexit__(self, *_: Any) -> None:
        await self.aclose()

    def close(self) -> None:
        return self._aexe.submit(self._conn.close)

    async def aclose(self) -> None:
        await self._aexe.asubmit(self._conn.close)

    def interrupt(self) -> None:
        self._conn.interrupt()

    async def with_conn(self, block: Callable[[Connection], T]) -> T:
        def cont() -> T:
            return block(self._conn)

        return await self._aexe.asubmit(cont)

    async def with_cursor(self, block: Callable[[Cursor], T]) -> T:
        def cont() -> T:
            cursor = self._conn.cursor()
            try:
                return block(cursor)
            finally:
                cursor.close()

        return await self._aexe.asubmit(cont)
