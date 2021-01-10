from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional, TypeVar, cast

T = TypeVar("T")


@asynccontextmanager
async def nullacontext(enter_result: Optional[T] = None) -> AsyncIterator[T]:
    yield cast(T, enter_result)
