from typing import AsyncIterable, AsyncIterator, TypeVar, Union

from .types import Void, VoidType

T = TypeVar("T")


def aiter(ait: AsyncIterable[T]) -> AsyncIterator[T]:
    return ait.__aiter__()


async def anext(ait: AsyncIterator[T], default: Union[T, VoidType] = Void) -> T:
    if isinstance(default, VoidType):
        return await ait.__anext__()
    else:
        try:
            return await ait.__anext__()
        except StopAsyncIteration:
            return default
