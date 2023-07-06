import sys
from asyncio import StreamWriter, gather
from asyncio.subprocess import DEVNULL, PIPE, create_subprocess_exec
from contextlib import suppress
from os import F_OK, environ
from shutil import which
from signal import Signals
from subprocess import CalledProcessError, CompletedProcess
from typing import (
    IO,
    AbstractSet,
    AsyncIterable,
    Callable,
    Iterable,
    Mapping,
    Optional,
    Union,
    cast,
)

from ..pathlib import AnyPath
from ..subprocess import SIGDED, kill_children
from ._prelude import pure

if sys.version_info < (3, 9):
    _R = CompletedProcess
else:
    _R = CompletedProcess[bytes]


async def _write(
    stdin: StreamWriter, data: Union[bytes, Iterable[bytes], AsyncIterable[bytes]]
) -> None:
    try:
        if isinstance(data, bytes):
            stdin.write(data)
        elif isinstance(data, Iterable):
            assert not isinstance(data, bytes)
            for d in data:
                stdin.write(d)
        else:
            async for d in data:
                stdin.write(d)
        await stdin.drain()
    finally:
        stdin.close()


async def call(
    arg0: AnyPath,
    *argv: AnyPath,
    kill_signal: Signals = SIGDED,
    capture_stdout: bool = True,
    capture_stderr: bool = True,
    stdin: Union[None, IO[bytes], bytes, Iterable[bytes], AsyncIterable[bytes]] = None,
    cwd: Optional[AnyPath] = None,
    env: Optional[Mapping[str, str]] = None,
    creationflags: int = 0,
    preexec_fn: Optional[Callable[[], None]] = None,
    check_returncode: AbstractSet[int] = frozenset((0,)),
) -> _R:
    if a0 := which(arg0):
        io_in = stdin if isinstance(stdin, IO) else (PIPE if stdin else DEVNULL)
        io_out = PIPE if capture_stdout else None
        io_err = PIPE if capture_stderr else None
        proc = await create_subprocess_exec(
            a0,
            *argv,
            start_new_session=True,
            creationflags=creationflags,
            preexec_fn=preexec_fn,
            stdin=io_in,
            stdout=io_out,
            stderr=io_err,
            cwd=cwd,
            env=None if env is None else {**environ, **env},
        )
        try:
            cmd = (arg0, *argv)

            i = (
                _write(cast(StreamWriter, proc.stdin), data=cast(bytes, stdin))
                if io_in == PIPE
                else pure(None)
            )
            o = proc.stdout.read() if proc.stdout else pure(b"")
            e = proc.stderr.read() if proc.stderr else pure(b"")

            code, _, stdout, stderr = await gather(
                proc.wait(),
                i,
                o,
                e,
            )

            if check_returncode and code not in check_returncode:
                raise CalledProcessError(
                    returncode=code,
                    cmd=cmd,
                    output=stdout if capture_stdout else None,
                    stderr=stderr.decode() if capture_stderr else None,
                )
            else:
                return CompletedProcess(
                    args=cmd, returncode=code, stdout=stdout, stderr=stderr
                )
        finally:
            with suppress(ProcessLookupError):
                try:
                    kill_children(proc.pid, sig=kill_signal)
                except PermissionError:
                    proc.kill()
            await proc.wait()
    elif a0 := which(arg0, mode=F_OK):
        raise PermissionError(a0)
    else:
        raise FileNotFoundError(arg0)
