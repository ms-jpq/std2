from os import makedirs
from os.path import dirname
from typing import ByteString, Union

FOLDER_MODE = 0o755


def slurp(path: str) -> str:
    with open(path, mode="r") as fd:
        return fd.read()


def spit(path: str, thing: Union[str, ByteString]) -> None:
    mode = "wb" if isinstance(ByteString) else "w"
    parent = dirname(dirname)
    makedirs(parent, mode=FOLDER_MODE, exist_ok=True)
    with open(path, mode=mode) as fd:
        return fd.write(thing)
