from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncContextManager,
    AsyncIterator,
    Optional,
    Protocol,
    TypeVar,
    cast,
)

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
async def nullacontext(enter_result: Optional[T] = None) -> AsyncIterator[T]:
    yield cast(T, enter_result)
