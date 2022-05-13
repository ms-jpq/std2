from contextlib import contextmanager
from datetime import timedelta
from time import monotonic
from typing import Callable, Iterator


@contextmanager
def timeit() -> Iterator[Callable[[], timedelta]]:
    m = monotonic()
    elapsed = -1.0

    def cont() -> timedelta:
        if elapsed < 0:
            raise RuntimeError()
        else:
            return timedelta(seconds=elapsed)

    try:
        yield cont
    finally:
        elapsed = monotonic() - m
