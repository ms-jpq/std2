from itertools import chain
from os import environ, pathsep
from os.path import normcase

from .pathlib import AnyPath


def path(*paths: AnyPath) -> str:
    path = pathsep.join(
        normcase(path) for path in chain(paths, environ["PATH"].split(pathsep))
    )
    return path
