from contextlib import suppress
from os import environ
from signal import Signals
from subprocess import DEVNULL, PIPE, CalledProcessError, CompletedProcess, Popen
from typing import AbstractSet, Mapping, Optional

from .pathlib import AnyPath

try:
    from signal import SIGKILL

    SIGDED = SIGKILL
except:
    from signal import SIGTERM

    SIGDED = SIGTERM


try:
    from os import getpgid, killpg

    def kill_children(pid: int, sig: Signals) -> None:
        killpg(getpgid(pid), sig)

except ImportError:
    from os import kill

    def kill_children(pid: int, sig: Signals) -> None:
        kill(pid, sig)


def call(
    prog: AnyPath,
    *args: AnyPath,
    kill_signal: Signals = SIGDED,
    capture_stdout: bool = True,
    capture_stderr: bool = True,
    stdin: Optional[bytes] = None,
    cwd: Optional[AnyPath] = None,
    env: Optional[Mapping[str, str]] = None,
    check: AbstractSet[int] = frozenset((0,))
) -> CompletedProcess[bytes]:
    with Popen(
        (prog, *args),
        start_new_session=True,
        stdin=PIPE if stdin is not None else DEVNULL,
        stdout=PIPE if capture_stdout else None,
        stderr=PIPE if capture_stderr else None,
        cwd=None if cwd is None else cwd,
        env=None if env is None else {**environ, **env},
    ) as proc:
        try:
            cmd = (prog, *args)
            stdout, stderr = proc.communicate(stdin)
            code = proc.wait()

            if check and code not in check:
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
            proc.wait()
