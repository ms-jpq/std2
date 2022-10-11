from abc import abstractmethod
from typing import (
    AsyncIterable,
    AsyncIterator,
    Callable,
    Optional,
    Protocol,
    TypeVar,
    Union,
)

from .types import Void, VoidType

_T = TypeVar("_T")
_T_ca = TypeVar("_T_ca", contravariant=True)


def aiter(ait: AsyncIterable[_T]) -> AsyncIterator[_T]:
    return ait.__aiter__()


async def anext(ait: AsyncIterator[_T], default: Union[_T, VoidType] = Void) -> _T:
    if isinstance(default, VoidType):
        return await ait.__anext__()
    else:
        try:
            return await ait.__anext__()
        except StopAsyncIteration:
            return default


class SupportsLT(Protocol[_T_ca]):
    @abstractmethod
    def __lt__(self, __other: _T_ca) -> bool:
        ...


_LT = TypeVar("_LT", bound=SupportsLT)


def clamp(
    lo: _LT,
    n: _LT,
    hi: _LT,
    key: Optional[Callable[[_LT], SupportsLT]] = None,
) -> _LT:
    l, h = (
        (min(lo, hi, key=key), max(lo, hi, key=key))
        if key
        else (min(lo, hi), max(lo, hi))
    )
    if key:
        return max(l, min(h, n, key=key), key=key)
    else:
        return max(l, min(h, n))
