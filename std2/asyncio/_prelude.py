from asyncio import get_running_loop
from asyncio.futures import Future
from asyncio.tasks import FIRST_COMPLETED, wait
from functools import partial
from itertools import chain
from typing import Any, Callable, Sequence, Tuple, TypeVar


T = TypeVar("T")


async def race(aw: Future[T], *aws: Future[T]) -> Tuple[T, Sequence[Future[T]]]:
    done, pending = await wait(tuple((aw, *aws)), return_when=FIRST_COMPLETED)
    ret = done.pop().result()
    return ret, tuple(chain(done, pending))


async def run_in_executor(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = get_running_loop()
    cont = partial(f, *args, **kwargs)
    return await loop.run_in_executor(None, cont)
