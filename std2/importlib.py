from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import PurePath
from sys import modules
from types import ModuleType
from typing import Iterator, Union, cast

from .itertools import deiter


def _gen_mod_name(path: Union[PurePath, str], top_level: Union[PurePath, str]) -> str:
    pp = PurePath(path)
    front_parts = (pp.parent / pp.stem).parts

    def cont() -> Iterator[str]:
        front_it = deiter(front_parts)
        top_level_it = deiter(PurePath(top_level).parts)
        while True:
            f_seg, t_seg = next(front_it, None), next(top_level_it, None)
            if f_seg and t_seg and f_seg == t_seg:
                pass
            elif f_seg and not t_seg:
                front_it.push_back(f_seg)
                break
            elif not f_seg and t_seg:
                top_level_it.push_back(t_seg)
                break
            else:
                front_it.push_back(cast(str, f_seg))
                top_level_it.push_back(cast(str, t_seg))
                break

        for _ in top_level_it:
            yield "."
        for f_seg in tuple(front_it) or front_parts[-1:]:
            yield "."
            yield f_seg

    return "".join(cont())


def module_from_path(
    path: Union[PurePath, str], top_level: Union[PurePath, str]
) -> ModuleType:
    name = _gen_mod_name(path, top_level=top_level)
    if name in modules:
        raise ImportError()
    else:
        spec = spec_from_file_location(name, path, submodule_search_locations=[])
        mod = module_from_spec(spec)
        modules[mod.__name__] = mod
        cast(Loader, spec.loader).exec_module(mod)
        return mod
