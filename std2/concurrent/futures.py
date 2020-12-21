from concurrent.futures import Future
from queue import SimpleQueue
from threading import Thread
from typing import Any, Callable, Optional, Tuple, TypeVar
from functools import partial

from ..asyncio import run_in_executor

T = TypeVar("T")


class AExecutor:
    def __init__(self, daemon: bool, name: Optional[str] = None) -> None:
        self._th = Thread(target=self._cont, daemon=daemon, name=name)
        self._ch: SimpleQueue[
            Optional[Tuple[Future, Callable[[], Any]]]
        ] = SimpleQueue()

    def _cont(self) -> None:
        while True:
            work = self._ch.get()
            if work:
                fut, func = work

                def cont() -> None:
                    try:
                        ret = func()
                    except BaseException as e:
                        fut.set_exception(e)
                    else:
                        fut.set_result(ret)

                cont()
            else:
                break

    def _submit(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> Future[T]:
        self._th.start()
        fut: Future[T] = Future()
        func = partial(f, *args, **kwargs)
        self._ch.put_nowait((fut, func))
        return fut

    def submit_sync(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        fut = self._submit(f, *args, **kwargs)
        return fut.result()

    async def submit(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        fut = self._submit(f, *args, **kwargs)
        return await run_in_executor(fut.result)

    async def shutdown(self) -> None:
        if self._th.is_alive():
            self._ch.put_nowait(None)
            await run_in_executor(self._th.join)