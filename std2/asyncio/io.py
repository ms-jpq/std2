from asyncio import StreamReader, StreamReaderProtocol, StreamWriter, get_running_loop
from asyncio.streams import FlowControlMixin
from typing import IO


async def reader(stream: IO) -> StreamReader:
    loop = get_running_loop()
    r = StreamReader(loop=loop)
    await loop.connect_read_pipe(
        lambda: StreamReaderProtocol(r, loop=loop), pipe=stream
    )
    return r


async def writer(stream: IO) -> StreamWriter:
    loop = get_running_loop()
    trans, proto = await loop.connect_write_pipe(
        lambda: FlowControlMixin(loop=loop), pipe=stream
    )
    w = StreamWriter(transport=trans, protocol=proto, reader=None, loop=loop)
    return w
