from importlib.util import module_from_spec, spec_from_file_location
from os.path import basename, splitext
from sys import modules
from types import ModuleType
from typing import Any, cast


def load_module(path: str) -> ModuleType:
    name, _ = splitext(basename(path))
    spec = spec_from_file_location(name, path, submodule_search_locations=[])
    mod = module_from_spec(spec)
    modules[mod.__name__] = mod
    cast(Any, spec.loader).exec_module(mod)
    return mod
