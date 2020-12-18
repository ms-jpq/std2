from contextlib import contextmanager
from time import monotonic
from typing import Callable, Iterator


@contextmanager
def timeit() -> Iterator[Callable[[], float]]:
    m = monotonic()
    elapsed = -1.0
    try:
        yield lambda: elapsed
    finally:
        elapsed = monotonic() - m
