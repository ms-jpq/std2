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

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


def chunk(it: Iterable[_T], n: int) -> Iterator[Sequence[_T]]:
    i = iter(it)
    return iter(lambda: tuple(islice(i, n)), ())


def chunk_into(seq: Sequence[_T], chunks: int = _CPUS) -> Iterator[Sequence[_T]]:
    n = ceil(len(seq) / chunks)
    yield from chunk(seq, n=n)


def interleave(it: Iterable[_T], val: _T) -> Iterator[_T]:
    for idx, v in enumerate(it):
        if idx:
            yield val
        yield v


def fst(t: Tuple[_T, Any]) -> _T:
    return t[0]


def snd(t: Tuple[Any, _T]) -> _T:
    return t[1]


def group_by(
    it: Iterable[_T], key: Callable[[_T], _K], val: Callable[[_T], _V]
) -> Mapping[_K, Sequence[_V]]:
    coll: MutableMapping[_K, MutableSequence[_V]] = {}

    for item in it:
        acc = coll.setdefault(key(item), [])
        acc.append(val(item))

    return coll


class deiter(Iterator[_T]):
    def __init__(self, it: Iterable[_T]) -> None:
        self._s: MutableSequence[_T] = []
        self._it = iter(it)

    def __iter__(self) -> Iterator[_T]:
        return self

    def __next__(self) -> _T:
        if self._s:
            return self._s.pop()
        else:
            return next(self._it)

    def push_back(self, *item: _T) -> None:
        self._s.extend(reversed(item))
