from typing import Optional, Sequence, TypeVar

T = TypeVar("T")
Index = int


def maybe_indexed(
    seq: Sequence[T], at: Index, default: Optional[T] = None
) -> Optional[T]:
    try:
        return seq[at]
    except IndexError:
        return default
