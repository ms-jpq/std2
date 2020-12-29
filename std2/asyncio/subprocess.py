from asyncio.subprocess import PIPE, create_subprocess_exec
from dataclasses import dataclass
from os import environ, getcwd
from subprocess import CalledProcessError
from typing import Mapping, Optional, Sequence, cast


@dataclass(frozen=True)
class ProcReturn:
    prog: str
    args: Sequence[str]
    code: int
    out: bytes
    err: str


async def call(
    prog: str,
    *args: str,
    stdin: Optional[bytes] = None,
    cwd: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
    expected_code: Optional[int] = None
) -> ProcReturn:
    proc = await create_subprocess_exec(
        prog,
        *args,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        cwd=getcwd() if cwd is None else cwd,
        env=environ if env is None else {**environ, **env}
    )
    stdout, stderr = await proc.communicate(stdin)
    code = cast(int, proc.returncode)

    if expected_code is not None and code != expected_code:
        raise CalledProcessError(
            returncode=code,
            cmd=tuple((prog, *args)),
            output=stdout,
            stderr=stderr.decode(),
        )
    else:
        return ProcReturn(
            prog=prog, args=args, code=code, out=stdout, err=stderr.decode()
        )
