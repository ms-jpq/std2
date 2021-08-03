from os import PathLike
from pathlib import Path, PurePath
from typing import Iterator, Optional, Union

AnyPath = Union[PathLike, str]


def walk(path: Path, dirs: bool = False) -> Iterator[Path]:
    for p in path.iterdir():
        if p.is_dir():
            if dirs:
                yield p
            yield from walk(p, dirs=dirs)
        else:
            yield p


def is_relative_to(origin: AnyPath, *other: AnyPath) -> bool:
    try:
        PurePath(origin).relative_to(*other)
        return True
    except ValueError:
        return False


def longest_common_path(p1: AnyPath, p2: AnyPath) -> Optional[PurePath]:
    def cont() -> Iterator[str]:
        for lhs, rhs in zip(PurePath(p1).parts, PurePath(p2).parts):
            if lhs == rhs:
                yield lhs
            else:
                break

    parts = tuple(cont())
    return PurePath(*parts) if parts else None
