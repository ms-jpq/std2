from typing import Sequence, TypeVar

_T = TypeVar("_T")


def maybe_indexed(seq: Sequence[_T], at: int, default: _T) -> _T:
    return seq[at] if at < len(seq) else default
