from asyncio import (
    StreamReader,
    StreamReaderProtocol,
    StreamWriter,
    gather,
    get_running_loop,
)
from asyncio.streams import FlowControlMixin
from dataclasses import dataclass
from os import devnull, fstat
from os.path import samestat
from sys import stderr, stdin, stdout
from typing import IO


@dataclass(frozen=True)
class Aio:
    stdin: StreamReader
    stdout: StreamWriter
    stderr: StreamWriter


async def stdio() -> Aio:
    with open(devnull) as fd:
        nsd = fstat(fd.fileno())
        if samestat(fstat(stdin.fileno()), nsd):
            raise RuntimeError()
        elif samestat(fstat(stdout.fileno()), nsd):
            raise RuntimeError()
        elif samestat(fstat(stderr.fileno()), nsd):
            raise RuntimeError()

    loop = get_running_loop()

    async def c1() -> StreamReader:
        sin = StreamReader(loop=loop)
        await loop.connect_read_pipe(lambda: StreamReaderProtocol(sin), pipe=stdin)
        return sin

    async def c2(stream: IO) -> StreamWriter:
        trans, proto = await loop.connect_write_pipe(FlowControlMixin, pipe=stream)
        w = StreamWriter(transport=trans, protocol=proto, reader=None, loop=loop)
        return w

    sdin, sdout, sderr = await gather(c1(), c2(stdout), c2(stderr))
    aio = Aio(stdin=sdin, stdout=sdout, stderr=sderr)
    return aio
