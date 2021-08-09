from asyncio.subprocess import DEVNULL, PIPE, create_subprocess_exec
from contextlib import suppress
from dataclasses import dataclass
from os import environ
from subprocess import CalledProcessError
from typing import AbstractSet, Mapping, Optional, Sequence

from ..pathlib import AnyPath

try:
    from os import getpgid, killpg
    from signal import SIGKILL

    def _kill(pid: int) -> None:
        killpg(getpgid(pid), SIGKILL)


except ImportError:
    from os import kill
    from signal import SIGTERM

    def _kill(pid: int) -> None:
        kill(pid, SIGTERM)


@dataclass(frozen=True)
class ProcReturn:
    prog: AnyPath
    args: Sequence[AnyPath]
    code: int
    out: bytes
    err: str


async def call(
    prog: AnyPath,
    *args: AnyPath,
    capture_stdout: bool = True,
    capture_stderr: bool = True,
    stdin: Optional[bytes] = None,
    cwd: Optional[AnyPath] = None,
    env: Optional[Mapping[str, str]] = None,
    check_returncode: AbstractSet[int] = frozenset((0,))
) -> ProcReturn:
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
        stdout, stderr = await proc.communicate(stdin)
        code = await proc.wait()

        if check_returncode and code not in check_returncode:
            raise CalledProcessError(
                returncode=code,
                cmd=(prog, *args),
                output=stdout if capture_stdout else None,
                stderr=stderr.decode() if capture_stderr else None,
            )
        else:
            return ProcReturn(
                prog=prog,
                args=args,
                code=code,
                out=stdout if capture_stdout else b"",
                err=stderr.decode() if capture_stderr else "",
            )
    finally:
        with suppress(ProcessLookupError):
            _kill(proc.pid)
        await proc.wait()
