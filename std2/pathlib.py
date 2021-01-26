from os import PathLike
from pathlib import Path, PurePath
from typing import Iterator, Optional, Union

AnyPath = Union[PathLike, str]


def walk(path: Path) -> Iterator[Path]:
    for p in path.iterdir():
        if p.is_dir():
            yield from walk(p)
        elif p.is_file():
            yield p


def is_relative_to(origin: AnyPath, *other: AnyPath) -> bool:
    try:
        PurePath(origin).relative_to(*other)
        return True
    except ValueError:
        return False


def longest_common_path(p1: AnyPath, p2: AnyPath) -> Optional[PurePath]:
    parts = tuple(
        lhs for lhs, rhs in zip(PurePath(p1).parts, PurePath(p2).parts) if lhs == rhs
    )
    return PurePath(*parts) if parts else None
