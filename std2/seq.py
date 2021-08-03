from typing import Sequence, TypeVar

T = TypeVar("T")


def maybe_indexed(seq: Sequence[T], at: int, default: T) -> T:
    return seq[at] if at < len(seq) else default
