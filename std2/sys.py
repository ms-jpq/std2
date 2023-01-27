from asyncio import create_task, sleep
from contextlib import asynccontextmanager
from os import getppid
from typing import AsyncIterator, Optional

from .asyncio import cancel


@asynccontextmanager
async def autodie(parent_id: Optional[int]) -> AsyncIterator[None]:
    async def die() -> None:
        ppid = getppid() if parent_id is None else parent_id
        while True:
            cppid = getppid()
            if cppid == 1 or cppid != ppid:
                raise SystemExit(1)
            else:
                await sleep(1)

    task = create_task(die())
    try:
        yield None
    finally:
        await cancel(task)
