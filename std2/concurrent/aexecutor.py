from __future__ import annotations

from concurrent.futures import Future
from functools import partial
from queue import SimpleQueue
from threading import Lock, Thread, _register_atexit  # type: ignore
from typing import Any, Callable, MutableSet, Optional, Tuple, TypeVar, cast

from ..asyncio import run_in_executor
from ..contextlib import AClosable, Closable

_lock = Lock()
_is_shutdown = False
_aexes: MutableSet[AExecutor] = set()


def _clean_up() -> None:
    global _is_shutdown
    with _lock:
        _is_shutdown = True
        aexes = tuple(_aexes)

    for aexe in aexes:
        aexe.close()


_register_atexit(_clean_up)


T = TypeVar("T")


class AExecutor(Closable, AClosable):
    def __init__(self, daemon: bool, name: Optional[str] = None) -> None:
        self._th = Thread(target=self._cont, daemon=daemon, name=name)
        self._ch: SimpleQueue = SimpleQueue()

        self._lock = Lock()
        self._is_alive = True

        with _lock:
            if _is_shutdown:
                raise RuntimeError()
            else:
                _aexes.add(self)

    def _cont(self) -> None:
        while True:
            work: Optional[Tuple[Future, Callable[[], Any]]] = self._ch.get()
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

    def submit(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        with _lock, self._lock:
            if _is_shutdown or not self._is_alive:
                raise RuntimeError()
            else:
                if not self._th.is_alive():
                    self._th.start()

                fut: Future = Future()
                func = partial(f, *args, **kwargs)
                self._ch.put((fut, func))
                return cast(T, fut.result())

    async def asubmit(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        return await run_in_executor(self.submit, f, *args, **kwargs)

    def close(self) -> None:
        with self._lock:
            self._is_alive = False

        if self._th.is_alive():
            self._ch.put(None)
            self._th.join()

        with _lock:
            if self in _aexes:
                _aexes.remove(self)

    async def aclose(self) -> None:
        await run_in_executor(self.close)
