from asyncio import get_running_loop
from typing import Callable, Any, TypeVar, AsyncIterator, Optional
from functools import partial


T = TypeVar("T")

async def anext(aiter: AsyncIterator[T], default: Optional[T] = None) -> Optional[T]:
    try:
        return await aiter.__anext__()
    except StopAsyncIteration:
        return default

async def run_in_executor(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = get_running_loop()
    cont = partial(f, *args, **kwargs)
    return await loop.run_in_executor(None, cont)