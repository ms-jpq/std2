from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import PurePath
from sys import modules
from types import ModuleType
from typing import AbstractSet, cast

from .pathlib import AnyPath


def _gen_mod_name(top_levels: AbstractSet[AnyPath], path: AnyPath) -> str:
    pp = PurePath(path)
    stem = pp.parent / pp.stem

    for top_level in map(PurePath, top_levels):
        if pp == top_level:
            raise ValueError()
        else:
            try:
                rel = stem.relative_to(top_level)
            except ValueError:
                pass
            else:
                return "." + ".".join(rel.parts)
    else:
        return ".".join(stem.parts)


def module_from_path(top_levels: AbstractSet[AnyPath], path: AnyPath) -> ModuleType:
    name = _gen_mod_name(top_levels, path=path)
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
