from ntpath import sep as ntsep
from os import PathLike, scandir, sep
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
from posixpath import sep as posixsep
from typing import Iterator, Optional, Union

AnyPath = Union[PathLike, str]

NT_ROT = PureWindowsPath(ntsep)
POSIX_ROOT = PurePosixPath(posixsep)
ROOT = PurePath(sep)


def walk(path: Union[PurePath, str], dirs: bool = False) -> Iterator[Path]:
    for s in scandir(path):
        p = Path(s)
        if s.is_dir():
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

    return PurePath(*parts) if (parts := tuple(cont())) else None
