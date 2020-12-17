from asyncio import get_running_loop
from asyncio.coroutines import iscoroutine
from asyncio.futures import Future
from asyncio.tasks import FIRST_COMPLETED, create_task, wait
from functools import partial
from itertools import chain
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    overload,
)

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


async def race(aw: Awaitable[T], *aws: Awaitable[T]) -> Tuple[T, Sequence[Future[T]]]:
    futs = tuple(create_task(a) if iscoroutine(a) else a for a in chain((aw,), aws))
    done, pending = await wait(futs, return_when=FIRST_COMPLETED)
    ret = done.pop().result()
    return ret, tuple(chain(done, pending))


async def run_in_executor(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = get_running_loop()
    cont = partial(f, *args, **kwargs)
    return await loop.run_in_executor(None, cont)
