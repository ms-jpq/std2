from typing import Iterable, Mapping, TypeVar

T = TypeVar("T")


def escape_with_prefix(stream: Iterable[T], escape: Mapping[T, T]) -> Iterable[T]:
    for unit in stream:
        if unit in escape:
            yield escape[unit]
        yield unit


def escape_with_replacement(stream: Iterable[T], escape: Mapping[T, T]) -> Iterable[T]:
    for unit in stream:
        if unit in escape:
            yield escape[unit]
        else:
            yield unit
