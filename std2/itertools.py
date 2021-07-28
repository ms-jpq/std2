from itertools import islice
from math import ceil
from multiprocessing import cpu_count
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Tuple,
    TypeVar,
)

_CPUS = cpu_count()

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def chunk(it: Iterable[T], n: int) -> Iterator[Sequence[T]]:
    i = iter(it)
    return iter(lambda: tuple(islice(i, n)), ())


def chunk_into(seq: Sequence[T], chunks: int = _CPUS) -> Iterator[Sequence[T]]:
    n = ceil(len(seq) / chunks)
    yield from chunk(seq, n=n)


def fst(t: Tuple[T, Any]) -> T:
    return t[0]


def snd(t: Tuple[Any, T]) -> T:
    return t[1]


def group_by(
    it: Iterable[T], key: Callable[[T], K], val: Callable[[T], V]
) -> Mapping[K, Sequence[V]]:
    coll: MutableMapping[K, MutableSequence[V]] = {}

    for item in it:
        acc = coll.setdefault(key(item), [])
        acc.append(val(item))

    return coll


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

