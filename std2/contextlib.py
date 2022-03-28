import sys
from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncIterator, Protocol, TypeVar

_T = TypeVar("_T")


class Closable(Protocol):
    @abstractmethod
    def close(self) -> None:
        ...


class AClosable(Protocol):
    @abstractmethod
    async def aclose(self) -> None:
        ...


_T2 = TypeVar("_T2", bound=AClosable)


if sys.version_info < (3, 10):

    @asynccontextmanager
    async def aclosing(thing: _T2) -> AsyncIterator[_T2]:
        try:
            yield thing
        finally:
            await thing.aclose()

else:
    from contextlib import aclosing as _aclosing

    aclosing = _aclosing


# TODO -- 3.10 has this on nullcontext
@asynccontextmanager
async def nullacontext(enter_result: _T) -> AsyncIterator[_T]:
    yield enter_result
