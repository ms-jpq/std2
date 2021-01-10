from contextlib import asynccontextmanager
from typing import AsyncIterator, TypeVar

T = TypeVar("T")


@asynccontextmanager
async def nullacontext(enter_result: T = None) -> AsyncIterator[T]:
    yield enter_result
