from collections.abc import Sequence
from typing import (
    Generic,
    Mapping,
    MutableSequence,
    Optional,
    SupportsIndex,
    TypeVar,
    Union,
    cast,
    overload,
)

_T = TypeVar("_T")


class defaultlist(Sequence, Generic[_T]):
    def __init__(
        self, defaultdict: Mapping[int, _T], len: Optional[int] = None
    ) -> None:
        self._len = (max(defaultdict) + 1 if defaultdict else 0) if len is None else len
        self._defaultdict = defaultdict

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
            i = index.__index__()
            ai = abs(i)
            idx = i % self._len if i < 0 and ai <= self._len else ai

            if idx >= self._len:
                raise IndexError()
            return cast(MutableSequence[_T], self._defaultdict[idx])
