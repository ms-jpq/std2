from asyncio import get_running_loop
from asyncio.futures import Future
from asyncio.tasks import FIRST_COMPLETED, wait
from functools import partial
from typing import Any, Callable, FrozenSet, MutableSet, Tuple, TypeVar, cast

from ..types import freeze

T = TypeVar("T")
_T2 = TypeVar("_T2", bound=Future)


async def race(aw: _T2, *aws: _T2) -> Tuple[_T2, FrozenSet[_T2], FrozenSet[_T2]]:
    r: Any = await wait(tuple((aw, *aws)), return_when=FIRST_COMPLETED)
    done, pending = cast(Tuple[MutableSet[_T2], MutableSet[_T2]], r)
    ret = done.pop()
    return ret, freeze(done), freeze(pending)


async def run_in_executor(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = get_running_loop()
    cont = partial(f, *args, **kwargs)
    return await loop.run_in_executor(None, cont)
