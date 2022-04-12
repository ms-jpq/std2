from contextlib import suppress
from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from os.path import normcase
from pathlib import PurePath
from sys import modules
from types import ModuleType
from typing import AbstractSet


def _gen_mod_name(
    top_level: PurePath, python_path: AbstractSet[PurePath], path: PurePath
) -> str:
    pp = PurePath(normcase(path))
    stem = pp.parent / pp.stem

    if pp in {top_level} | python_path:
        raise ValueError()
    else:
        with suppress(ValueError):
            rel = stem.relative_to(top_level)
            return "." + ".".join(rel.parts)

        for python_p in python_path:
            with suppress(ValueError):
                rel = stem.relative_to(python_p)
                return ".".join(rel.parts)
        else:
            raise ValueError()


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


def module_from_path(
    top_level: PurePath, python_path: AbstractSet[PurePath], path: PurePath
) -> ModuleType:
    try:
        name = _gen_mod_name(top_level, python_path=python_path, path=path)
    except ValueError:
        name = ""

    if not name:
        raise ImportError()
    elif name in modules:
        raise ImportError()
    else:
        mod = ld_mod(name, path)
        return mod
