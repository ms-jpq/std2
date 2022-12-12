from asyncio import StreamReader, StreamReaderProtocol, StreamWriter, get_running_loop
from asyncio.streams import FlowControlMixin
from io import BytesIO
from typing import AsyncIterable, Awaitable, BinaryIO, Tuple


async def reader(stream: BinaryIO) -> StreamReader:
    loop = get_running_loop()
    r = StreamReader(loop=loop)
    await loop.connect_read_pipe(
        lambda: StreamReaderProtocol(r, loop=loop), pipe=stream
    )
    return r


async def writer(stream: BinaryIO) -> StreamWriter:
    loop = get_running_loop()
    trans, proto = await loop.connect_write_pipe(
        lambda: FlowControlMixin(loop=loop), pipe=stream
    )
    w = StreamWriter(transport=trans, protocol=proto, reader=None, loop=loop)
    return w


def io(aiterable: AsyncIterable[bytes]) -> Tuple[BinaryIO, Awaitable[None]]:
    io = BytesIO()

    async def cont() -> None:
        async for frame in aiterable:
            io.write(frame)

    return io, cont()
