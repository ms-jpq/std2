from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from os import pathsep
from os.path import relpath, splitext
from sys import modules
from types import ModuleType
from typing import cast


def load_module(path: str, top_level: str) -> ModuleType:
    front, _ = splitext(path)
    rel_name = relpath(front, start=top_level)
    name = "".join("." if c == pathsep else c for c in rel_name)
    spec = spec_from_file_location(name, path, submodule_search_locations=[])
    mod = module_from_spec(spec)
    modules[mod.__name__] = mod
    cast(Loader, spec.loader).exec_module(mod)
    return mod
