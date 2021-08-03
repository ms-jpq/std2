from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from os import sep
from os.path import relpath
from pathlib import PurePath
from sys import modules
from types import ModuleType
from typing import Iterator, cast

from .pathlib import AnyPath


def _gen_mod_name(top_level: AnyPath, path: AnyPath) -> str:
    pp, tl = PurePath(path), PurePath(top_level)
    if pp == tl:
        raise ValueError()
    else:

        def cont() -> Iterator[str]:
            stem = pp.parent / pp.stem
            rel = relpath(stem, start=tl)
            print(rel, [path, top_level])
            for part in rel.split(sep):
                if part == ".":
                    yield ""
                elif part == "..":
                    yield "."
                else:
                    yield part

    return ".".join(cont())


def module_from_path(top_level: AnyPath, path: AnyPath) -> ModuleType:
    name = _gen_mod_name(top_level, path=path)
    if name in modules:
        raise ImportError()
    else:
        spec = spec_from_file_location(name, path, submodule_search_locations=[])
        if not spec:
            raise ImportError()
        else:
            mod = module_from_spec(spec)
            modules[mod.__name__] = mod
            cast(Loader, spec.loader).exec_module(mod)
            return mod
