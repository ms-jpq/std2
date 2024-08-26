from collections import defaultdict
from collections.abc import MutableSequence as MS
from itertools import chain, count
from typing import (
    Callable,
    Generic,
    Iterable,
    MutableMapping,
    MutableSequence,
    SupportsIndex,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

_T = TypeVar("_T")


class defaultlist(MS, Generic[_T]):
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

    @overload
    def __getitem__(self, index: SupportsIndex) -> _T: ...
    @overload
    def __getitem__(self, index: slice) -> MutableSequence[_T]: ...
    def __getitem__(
        self, index: Union[slice, SupportsIndex]
    ) -> Union[MutableSequence[_T], _T]:
        if isinstance(index, slice):
            return [self._defaultdict[idx] for idx in range(*index.indices(self._len))]
        else:
            idx = self._idx(index)
            if idx >= self._len:
                raise IndexError()
            return cast(MutableSequence[_T], self._defaultdict[idx])

    @overload
    def __setitem__(self, index: SupportsIndex, value: _T) -> None: ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None: ...
    def __setitem__(
        self, index: Union[slice, SupportsIndex], value: Union[Iterable[_T], _T]
    ) -> None:
        if isinstance(index, slice):
            loop: Iterable[Tuple[int, _T]] = zip(
                chain(range(*index.indices(self._len)), count(self._len)),
                cast(Iterable[_T], value),
            )
            if index.start is None and index.stop is None:
                self.clear()
            elif index.start is None:
                for idx in range(0, index.stop, index.step):
                    del self._defaultdict[idx]
            elif index.stop is None:
                for idx in range(index.start, self._len, index.step):
                    del self._defaultdict

        else:
            idx = self._idx(index)
            loop = ((idx, cast(_T, value)),)

        for idx, val in loop:
            self._len = max(self._len, idx + 1)
            self._defaultdict[idx] = val

    def __delitem__(self, index: Union[slice, SupportsIndex]) -> None:
        if isinstance(index, slice):
            for idx in range(*index.indices(self._len)):
                del self._defaultdict[idx]
        else:
            idx = self._idx(index)
            if idx >= self._len:
                raise IndexError()
            del self._defaultdict[idx]

    def clear(self) -> None:
        self._len = 0
        self._defaultdict.clear()

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
