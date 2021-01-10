from contextlib import contextmanager
from time import monotonic
from typing import Callable, Iterator


@contextmanager
def timeit() -> Iterator[Callable[[], float]]:
    m = monotonic()
    elapsed = -1.0

    def cont() -> float:
        if elapsed < 0:
            raise RuntimeError()
        else:
            return elapsed

    try:
        yield cont
    finally:
        elapsed = monotonic() - m
