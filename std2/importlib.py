from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmodulename
from os.path import normcase
from pathlib import PurePath
from sys import modules
from types import ModuleType


def ld_mod(name: str, path: PurePath) -> ModuleType:
    spec = spec_from_file_location(name, location=path, submodule_search_locations=[])
    if not spec:
        raise ImportError()
    else:
        mod = module_from_spec(spec)
        modules[mod.__name__] = mod
        assert isinstance(spec.loader, Loader)
        spec.loader.exec_module(mod)
        return mod


def ld_mod_from_path(path: PurePath) -> ModuleType:
    if name := getmodulename(normcase(path)):
        if name in modules:
            raise ImportError()
        else:
            mod = ld_mod(name, path)
            return mod
    else:
        raise ImportError()
