from enum import Enum, auto
from platform import system


class OS(Enum):
    bsd = auto()
    java = auto()
    linux = auto()
    macos = auto()
    windows = auto()


def _os() -> OS:
    sys = system().casefold()
    if sys == "linux":
        return OS.linux
    elif sys == "darwin":
        return OS.macos
    elif sys == "windows":
        return OS.windows
    elif sys == "freebsd":
        return OS.bsd
    elif sys == "java":
        return OS.java
    else:
        assert False, sys


os = _os()
