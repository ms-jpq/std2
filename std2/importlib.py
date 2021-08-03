from contextlib import suppress
from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import PurePath
from sys import modules
from types import ModuleType
from typing import AbstractSet, cast

from .pathlib import AnyPath


def _gen_mod_name(
    top_level: AnyPath, python_path: AbstractSet[AnyPath], path: AnyPath
) -> str:
    pp = PurePath(path)
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


def module_from_path(
    top_level: AnyPath, python_path: AbstractSet[AnyPath], path: AnyPath
) -> ModuleType:
    try:
        name = _gen_mod_name(top_level, python_path=python_path, path=path)
    except ValueError:
        raise ImportError()
    else:
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
