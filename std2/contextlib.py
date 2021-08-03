from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncIterator, Protocol, TypeVar

T = TypeVar("T")


class Closable(Protocol):
    @abstractmethod
    def close(self) -> None:
        ...


class AClosable(Protocol):
    @abstractmethod
    async def aclose(self) -> None:
        ...


_T2 = TypeVar("_T2", bound=AClosable)


@asynccontextmanager
async def aclosing(thing: _T2) -> AsyncIterator[_T2]:
    try:
        yield thing
    finally:
        await thing.aclose()


@asynccontextmanager
async def nullacontext(enter_result: T) -> AsyncIterator[T]:
    yield enter_result
