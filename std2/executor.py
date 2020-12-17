from concurrent.futures import Future
from queue import SimpleQueue
from threading import Thread
from typing import Any, Callable, TypeVar

from .asyncio import run_in_executor

T = TypeVar("T")


class Executor:
    def __init__(self) -> None:
        self._th = Thread(target=self._cont, daemon=True)
        self._ch: SimpleQueue = SimpleQueue()

    def _cont(self) -> None:
        while True:
            f = self._ch.get()
            f()


    def run_sync(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        self._th.start()

        fut: Future[T] = Future()

        def cont() -> None:
            try:
                ret = f(*args, **kwargs)
                fut.set_result(ret)
            except BaseException as e:
                fut.set_exception(e)

        self._ch.put_nowait(cont)
        return fut.result()


    async def run(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        self._th.start()

        fut: Future = Future()

        def cont() -> None:
            try:
                ret = f(*args, **kwargs)
                fut.set_result(ret)
            except BaseException as e:
                fut.set_exception(e)

        self._ch.put_nowait(cont)
        return await run_in_executor(fut.result)
