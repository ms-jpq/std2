import sys
from asyncio.subprocess import DEVNULL, PIPE, create_subprocess_exec
from contextlib import suppress
from os import environ
from signal import Signals
from subprocess import CalledProcessError, CompletedProcess
from typing import AbstractSet, Mapping, Optional

from ..pathlib import AnyPath
from ..subprocess import SIGDED, kill_children

if sys.version_info < (3, 9):
    _R = CompletedProcess
else:
    _R = CompletedProcess[bytes]


async def call(
    prog: AnyPath,
    *args: AnyPath,
    kill_signal: Signals = SIGDED,
    capture_stdout: bool = True,
    capture_stderr: bool = True,
    stdin: Optional[bytes] = None,
    cwd: Optional[AnyPath] = None,
    env: Optional[Mapping[str, str]] = None,
    check_returncode: AbstractSet[int] = frozenset((0,))
) -> _R:
    proc = await create_subprocess_exec(
        prog,
        *args,
        start_new_session=True,
        stdin=PIPE if stdin is not None else DEVNULL,
        stdout=PIPE if capture_stdout else None,
        stderr=PIPE if capture_stderr else None,
        cwd=None if cwd is None else cwd,
        env=None if env is None else {**environ, **env},
    )
    try:
        cmd = (prog, *args)
        stdout, stderr = await proc.communicate(stdin)
        code = await proc.wait()

        if check_returncode and code not in check_returncode:
            raise CalledProcessError(
                returncode=code,
                cmd=cmd,
                output=stdout if capture_stdout else None,
                stderr=stderr.decode() if capture_stderr else None,
            )
        else:
            return CompletedProcess(
                args=cmd,
                returncode=code,
                stdout=stdout if capture_stdout else b"",
                stderr=stderr if capture_stderr else b"",
            )
    finally:
        with suppress(ProcessLookupError):
            try:
                kill_children(proc.pid, sig=kill_signal)
            except PermissionError:
                proc.kill()
        await proc.wait()
