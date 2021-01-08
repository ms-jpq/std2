from concurrent.futures import ALL_COMPLETED, Future, wait
from typing import TypeVar, cast

T = TypeVar("T")


def gather(*futs: Future) -> T:
    wait(futs, return_when=ALL_COMPLETED)
    return cast(T, tuple(fut.result() for fut in futs))
