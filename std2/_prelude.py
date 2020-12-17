from typing import AsyncIterator, ByteString, Union, TypeVar, overload

T = TypeVar("T")
U = TypeVar("U")


@overload
async def anext(ait: AsyncIterator[T]) -> T:
    ...


@overload
async def anext(ait: AsyncIterator[T], default: U) -> Union[T, U]:
    ...


async def anext(ait: AsyncIterator[T], *args: U) -> Union[T, U]:
    if len(args) == 0:
        return await ait.__anext__()
    elif len(args) == 1:
        try:
            return await ait.__anext__()
        except StopAsyncIteration:
            return next(iter(args))
    else:
        raise ValueError()


def slurp(path: str) -> str:
    with open(path) as fd:
        return fd.read()


def spit(path: str, thing: Union[str, ByteString]) -> None:
    pass
