from typing import Iterable, Iterator, MutableSequence, TypeVar

T = TypeVar("T")


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