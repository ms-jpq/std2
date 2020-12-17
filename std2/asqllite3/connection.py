from __future__ import annotations

from asyncio.locks import Lock
from sqlite3 import Connection, Cursor, Row, connect
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    Iterable,
    Optional,
    Type,
    TypeVar,
    cast,
)

from ..concurrent.futures import Executor
from .cursor import ACursor
from .types import SQL_TYPES

T = TypeVar("T")


class AConnection(AsyncContextManager[None]):
    def __init__(self, database: str = ":memory:") -> None:
        self._exe = Executor()
        self._lock = Lock()

        def cont() -> Connection:
            conn = connect(database, isolation_level=None)
            conn.row_factory = Row
            return conn

        self._conn = self._exe.run_sync(cont)

    async def __aenter__(self) -> None:
        await self._lock.acquire()

    async def __aexit__(self, *_: Any) -> None:
        self._lock.release()

    @property
    def isolation_level(self) -> Optional[str]:
        return cast(Optional[str], self._conn.isolation_level)

    @property
    def in_transaction(self) -> bool:
        return cast(bool, self._conn.in_transaction)

    @property
    def row_factory(self) -> Optional[Type]:
        return cast(Optional[Type], self._conn.row_factory)

    @property
    def total_changes(self) -> int:
        return cast(int, self._conn.total_changes)

    async def cursor(self) -> ACursor:
        def cont() -> ACursor:
            cursor = self._conn.cursor()
            return ACursor(self._exe, cursor=cursor)

        return await self._exe.run(cont)

    async def commit(self) -> None:
        return await self._exe.run(self._conn.commit)

    async def rollback(self) -> None:
        return await self._exe.run(self._conn.rollback)

    async def close(self) -> None:
        return await self._exe.run(self._conn.close)

    async def execute(self, sql: str, params: Iterable[SQL_TYPES] = ()) -> ACursor:
        def cont() -> ACursor:
            cursor = self._conn.execute(sql, params)
            return ACursor(self._exe, cursor=cursor)

        return await self._exe.run(cont)

    async def executemany(
        self, sql: str, params: Iterable[Iterable[SQL_TYPES]] = ()
    ) -> ACursor:
        def cont() -> ACursor:
            cursor = self._conn.executemany(sql, params)
            return ACursor(self._exe, cursor=cursor)

        return await self._exe.run(cont)

    async def executescript(self, script: str) -> ACursor:
        def cont() -> ACursor:
            cursor = self._conn.executescript(script)
            return ACursor(self._exe, cursor=cursor)

        return await self._exe.run(cont)

    async def create_function(
        self,
        name: str,
        num_params: int,
        func: Callable[..., SQL_TYPES],
        deterministic: bool,
    ) -> None:
        def cont() -> None:
            self._conn.create_function(
                name, num_params=num_params, deterministic=deterministic, func=func
            )

        return await self._exe.run(cont)

    async def create_aggregate(
        self, name: str, num_params: int, aggregate_class: Type
    ) -> None:
        def cont() -> None:
            self._conn.create_aggregate(
                name, num_params=num_params, aggregate_class=aggregate_class
            )

        return await self._exe.run(cont)

    async def create_collation(
        self, name: str, callable: Callable[..., SQL_TYPES]
    ) -> None:
        def cont() -> None:
            self._conn.create_collation(name, callable=callable)

        return await self._exe.run(cont)

    def interrupt(self) -> None:
        self._conn.interrupt()

    async def with_raw_cursor(self, block: Callable[[Cursor], T]) -> T:
        def cont() -> T:
            cursor = self._conn.cursor()
            try:
                return block(cursor)
            finally:
                cursor.close()

        return await self._exe.run(cont)
