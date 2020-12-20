from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from os.path import abspath, basename, splitext
from sys import modules
from types import ModuleType
from typing import Iterator, cast

from .itertools import deiter
from .os.path import segments


def _gen_mod_name(path: str, top_level: str) -> str:
    front, _ = splitext(path)
    front_segments = tuple((basename(s) for s in segments(front)))

    def cont() -> Iterator[str]:
        front_it = deiter(front_segments)
        top_level_it = deiter((basename(s) for s in segments(top_level)))
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
        for f_seg in tuple(front_it) or front_segments[-1:]:
            yield "."
            yield f_seg

    return "".join(cont())


def module_from_path(path: str, top_level: str) -> ModuleType:
    abp = abspath(path)
    name = _gen_mod_name(abp, top_level=abspath(top_level))
    spec = spec_from_file_location(name, abp, submodule_search_locations=[])
    mod = module_from_spec(spec)
    modules[mod.__name__] = mod
    cast(Loader, spec.loader).exec_module(mod)
    return mod
