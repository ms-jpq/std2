from concurrent.futures import ALL_COMPLETED, Future, wait
from typing import TypeVar

T = TypeVar("T")


def gather(*futs: Future) -> T:
    wait(futs, return_when=ALL_COMPLETED)
    return tuple(fut.result() for fut in futs)
