from abc import abstractmethod
from contextlib import asynccontextmanager, contextmanager
from logging import Logger
from typing import Any, AsyncContextManager, AsyncIterator, Iterator, Protocol, TypeVar

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


class aclosing(AsyncContextManager[_T2]):
    def __init__(self, thing: _T2) -> None:
        self._thing = thing

    async def __aenter__(self) -> _T2:
        return self._thing

    async def __aexit__(self, *_: Any) -> None:
        await self._thing.aclose()


@asynccontextmanager
async def nullacontext(enter_result: T) -> AsyncIterator[T]:
    yield enter_result


@contextmanager
def log_exc(log: Logger) -> Iterator[None]:
    try:
        yield None
    except Exception as e:
        log.exception("%s", e)
