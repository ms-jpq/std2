from contextlib import closing
from io import BufferedIOBase
from typing import Iterator


def io_read(io: BufferedIOBase, buf: int) -> Iterator[bytes]:
    with closing(io):
        chunk = io.read(buf)
        while chunk:
            yield chunk
            chunk = io.read(buf)
