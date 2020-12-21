from atexit import register
from concurrent.futures import Future
from functools import partial
from queue import SimpleQueue
from threading import Thread
from typing import Any, Callable, MutableSequence, Optional, Tuple, TypeVar

from ..asyncio import run_in_executor

T = TypeVar("T")

_threads: MutableSequence[Thread] = []
_exiting = False


def _clean_up() -> None:
    global _exiting
    _exiting = True
    for thread in _threads:
        thread.join()


register(_clean_up)


class AExecutor:
    def __init__(self, daemon: bool, name: Optional[str] = None) -> None:
        self._th = Thread(target=self._cont, daemon=daemon, name=name)
        self._ch: SimpleQueue[
            Optional[Tuple[Future, Callable[[], Any]]]
        ] = SimpleQueue()
        _threads.append(self._th)

    def _cont(self) -> None:
        while not _exiting:
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
