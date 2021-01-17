from collections.abc import Mapping
from locale import strxfrm
from typing import Any, Mapping

from .types import is_seq


def recur_sort(data: Any) -> Any:
    if isinstance(data, Mapping):
        return {k: recur_sort(data[k]) for k in sorted(data, key=strxfrm)}
    elif is_seq(data):
        return tuple(recur_sort(el) for el in data)
    else:
        return data


def _merge(ds1: Any, ds2: Any, replace: bool = False) -> Any:
    if isinstance(ds1, Mapping) and isinstance(ds2, Mapping):
        append = {k: _merge(ds1.get(k), v, replace) for k, v in ds2.items()}
        return {**ds1, **append}
    if is_seq(ds1) and is_seq(ds2):
        if replace:
            return ds2
        else:
            return (*ds1, *ds2)
    else:
        return ds2


def merge(ds1: Any, *dss: Any, replace: bool = False) -> Any:
    res = ds1
    for ds2 in dss:
        res = _merge(res, ds2, replace=replace)
    return res
