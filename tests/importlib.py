from os import sep
from pathlib import PurePath
from unittest import TestCase

from ..std2.importlib import _gen_mod_name, module_from_path
from ._consts import TOP_LEVEL

_ROOT = PurePath(sep)


class ModFromPath(TestCase):
    def test_1(self) -> None:
        setup_py = TOP_LEVEL / "__init__.py"

        mod = module_from_path(TOP_LEVEL, python_path=set(), path=setup_py)
        self.assertEqual(mod.__name__, ".__init__")

    def test_2(self) -> None:
        mod = _ROOT / "d" / "e"
        name = _gen_mod_name(_ROOT, python_path=set(), path=mod)
        self.assertEqual(name, ".d.e")

    def test_3(self) -> None:
        mod = _ROOT / "a" / "b"
        with self.assertRaises(ValueError):
            _gen_mod_name(TOP_LEVEL, python_path=set(), path=mod)

    def test_4(self) -> None:
        mod = _ROOT / "a" / "b"
        name = _gen_mod_name(TOP_LEVEL, python_path={_ROOT}, path=mod)
        self.assertEqual(name, "a.b")
