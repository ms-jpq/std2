from asyncio.subprocess import PIPE, create_subprocess_exec
from subprocess import CalledProcessError
from dataclasses import dataclass
from os import environ, getcwd
from typing import Mapping, Optional, cast


@dataclass(frozen=True)
class ProcReturn:
    code: int
    out: str
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
        stdout=PIPE,
        stderr=PIPE,
        cwd=getcwd() if cwd is None else cwd,
        env=environ if env is None else {**environ, **env}
    )
    stdout, stderr = await proc.communicate(stdin)
    code = cast(int, proc.returncode)

    if expected_code is not None and code != expected_code:
        raise CalledProcessError(
            returncode=code, cmd=tuple((prog, *args)), output=stdout, stderr=stderr
        )
    else:
        return ProcReturn(code=code, out=stdout.decode(), err=stderr.decode())
