from collections.abc import Mapping
from itertools import chain
from locale import strxfrm
from typing import AbstractSet, Any, Callable, Mapping, Optional

from .types import is_iterable_not_str


def _order(key: Any) -> Any:
    if isinstance(key, str):
        return strxfrm(key)
    else:
        return key


def recur_sort(
    data: Any, key: Optional[Callable[[Any], Any]] = None, reverse: bool = False
) -> Any:
    order = key or _order

    if isinstance(data, Mapping):
        return {
            k: recur_sort(data[k], key=order, reverse=reverse)
            for k in sorted(data, key=order, reverse=reverse)
        }
    elif isinstance(data, AbstractSet):
        return tuple(sorted(data, key=key, reverse=reverse))
    elif is_iterable_not_str(data):
        return tuple(recur_sort(el, key=order, reverse=reverse) for el in data)
    else:
        return data


def _merge(ds1: Any, ds2: Any, replace: bool) -> Any:
    if isinstance(ds1, Mapping) and isinstance(ds2, Mapping):
        append = {k: _merge(ds1.get(k), v, replace) for k, v in ds2.items()}
        return {**ds1, **append}
    elif isinstance(ds1, AbstractSet) and isinstance(ds2, AbstractSet):
        return frozenset(chain(ds1, ds2))
    elif is_iterable_not_str(ds1) and is_iterable_not_str(ds2):
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
