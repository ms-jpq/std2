from enum import Enum, auto
from sys import platform


class OS(Enum):
    linux = auto()
    macos = auto()
    windows = auto()


def _os() -> OS:
    if platform.startswith("linux"):
        return OS.linux
    elif platform.startswith("darwin"):
        return OS.macos
    elif platform.startswith("win"):
        return OS.windows
    else:
        assert False, platform


os = _os()
