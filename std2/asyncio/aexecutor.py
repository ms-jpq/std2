from __future__ import annotations

from concurrent.futures import Future
from functools import partial
from queue import SimpleQueue
from threading import Lock, Thread, _register_atexit  # type: ignore
from typing import Any, Callable, MutableSet, Optional, Tuple, TypeVar, cast

from ..asyncio import run_in_executor

_lock = Lock()
_is_shutdown = False
_aexes: MutableSet[AExecutor] = set()


def _clean_up() -> None:
    global _is_shutdown
    with _lock:
        _is_shutdown = True
        aexes = tuple(_aexes)

    for aexe in aexes:
        aexe.shutdown_sync()


_register_atexit(_clean_up)


T = TypeVar("T")


class AExecutor:
    def __init__(self, daemon: bool, name: Optional[str] = None) -> None:
        self._th = Thread(target=self._cont, daemon=daemon, name=name)
        self._ch: SimpleQueue = SimpleQueue()
        with _lock:
            if _is_shutdown:
                raise RuntimeError()
            else:
                _aexes.add(self)

    def _cont(self) -> None:
        while not _is_shutdown:
            work: Optional[Tuple[Future, Callable[[], T]]] = self._ch.get()
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

    def _submit(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> Future:
        self._th.start()
        fut: Future = Future()
        func = partial(f, *args, **kwargs)
        self._ch.put((fut, func))
        return fut

    def submit_sync(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        fut = self._submit(f, *args, **kwargs)
        return cast(T, fut.result())

    async def submit(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        fut = self._submit(f, *args, **kwargs)
        return await run_in_executor(fut.result)

    def shutdown_sync(self) -> None:
        if self._th.is_alive():
            self._ch.put(None)
            self._th.join()

        with _lock:
            if self in _aexes:
                _aexes.remove(self)

    async def shutdown(self) -> None:
        await run_in_executor(self.shutdown_sync)
