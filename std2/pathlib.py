from pathlib import Path
from typing import Iterator


def walk(path: Path) -> Iterator[Path]:
    for p in path.iterdir():
        if p.is_dir():
            yield from walk(p)
        elif p.is_file():
            yield p
