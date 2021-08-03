from typing import AsyncIterable, AsyncIterator, TypeVar, Union

from .types import Void, VoidType

_T = TypeVar("_T")


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
