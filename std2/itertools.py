from itertools import islice
from typing import Iterable, Iterator, MutableSequence, Sequence, TypeVar

T = TypeVar("T")


def take(it: Iterable[T], n: int) -> Sequence[T]:
    return tuple(islice(it, n))


def chunk(it: Iterable[T], n: int) -> Iterator[Sequence[T]]:
    return iter(lambda: take(it, n), ())


class deiter(Iterator[T]):
    def __init__(self, it: Iterable[T]) -> None:
        self._s: MutableSequence[T] = []
        self._it = iter(it)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self._s:
            return self._s.pop()
        else:
            return next(self._it)

    def push_back(self, *item: T) -> None:
        self._s.extend(reversed(item))
