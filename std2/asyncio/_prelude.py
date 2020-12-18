from asyncio import get_running_loop
from asyncio.coroutines import iscoroutine
from asyncio.futures import Future
from asyncio.tasks import FIRST_COMPLETED, create_task, wait
from functools import partial
from itertools import chain
from time import monotonic
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from ..types import Void, VoidType

T = TypeVar("T")
U = TypeVar("U")


async def anext(ait: AsyncIterator[T], default: Union[U, VoidType]) -> Union[T, U]:
    if default is Void:
        return await ait.__anext__()
    else:
        try:
            return await ait.__anext__()
        except StopAsyncIteration:
            return cast(U, default)


async def race(aw: Awaitable[T], *aws: Awaitable[T]) -> Tuple[T, Sequence[Future[T]]]:
    futs = tuple(create_task(a) if iscoroutine(a) else a for a in chain((aw,), aws))
    done, pending = await wait(futs, return_when=FIRST_COMPLETED)
    ret = done.pop().result()
    return ret, tuple(chain(done, pending))


async def timer(delay: float) -> AsyncIterator[float]:
    yield 0.0
    t = monotonic()
    while True:
        t = monotonic()
        yield t


async def run_in_executor(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = get_running_loop()
    cont = partial(f, *args, **kwargs)
    return await loop.run_in_executor(None, cont)
