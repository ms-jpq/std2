from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Iterator


@contextmanager
def nil_manager() -> Iterator[None]:
    yield None


@asynccontextmanager
async def nil_amanager() -> AsyncIterator[None]:
    yield None
