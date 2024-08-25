from collections import defaultdict
from collections.abc import MutableSequence
from typing import (
    Callable,
    Generic,
    Iterable,
    MutableMapping,
    SupportsIndex,
    TypeVar,
    cast,
)

_T = TypeVar("_T")


class defaultlist(MutableSequence, Generic[_T]):
    def __init__(self, default_factory: Callable[[], _T]) -> None:
        self._len = 0
        self.default_factory = default_factory
        self._defaultdict: MutableMapping[int, _T] = defaultdict(default_factory)

    def _idx(self, index: SupportsIndex) -> int:
        i = index.__index__()
        ai = abs(i)
        idx = i % self._len if i < 0 and ai <= self._len else ai
        return idx

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, index: slice | SupportsIndex) -> MutableSequence[_T]:
        if isinstance(index, slice):
            return [self._defaultdict[idx] for idx in range(*index.indices(self._len))]
        else:
            idx = self._idx(index)
            if idx >= self._len:
                raise IndexError
            return cast(MutableSequence[_T], self._defaultdict[idx])

    def __setitem__(self, index: slice | SupportsIndex, value: Iterable[_T]) -> None:
        if isinstance(index, slice):
            for idx, val in zip(range(*index.indices(self._len)), value):
                self._len = max(self._len, idx + 1)
                self._defaultdict[idx] = val
        else:
            idx = self._idx(index)
            self._defaultdict[idx] = cast(_T, value)

    def __delitem__(self, index: slice | SupportsIndex) -> None:
        if isinstance(index, slice):
            for idx in range(*index.indices(self._len)):
                del self._defaultdict[idx]
        else:
            idx = self._idx(index)
            del self._defaultdict[idx]

    def insert(self, index: SupportsIndex, value: _T) -> None:
        idx = self._idx(index)
        if idx >= self._len:
            self._defaultdict[self._len] = value
        else:
            for i in range(self._len, idx, -1):
                if (i - 1) in self._defaultdict:
                    self._defaultdict[i] = self._defaultdict[i - 1]
            self._defaultdict[idx] = value

        self._len = self._len + 1
