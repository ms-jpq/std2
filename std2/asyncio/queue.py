import sys
from asyncio.queues import Queue
from typing import Any, AsyncIterator, TypeVar

if sys.version_info < (3, 9):

    async def to_iter(queue: Queue) -> AsyncIterator[Any]:
        while True:
            yield await queue.get()

else:
    _T = TypeVar("_T")

    async def to_iter(queue: Queue[_T]) -> AsyncIterator[_T]:
        while True:
            yield await queue.get()
