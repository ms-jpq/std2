from pathlib import PurePath
from unittest import TestCase

from ..std2.importlib import _gen_mod_name, module_from_path
from ._consts import TOP_LEVEL


class ModFromPath(TestCase):
    def test_1(self) -> None:
        setup_py = PurePath(TOP_LEVEL, "__init__.py")

        mod = module_from_path({TOP_LEVEL}, path=setup_py)
        self.assertEqual(mod.__name__, ".__init__")

    def test_2(self) -> None:
        common = PurePath(*"abc")
        mod = PurePath(common, *"de")
        top_level = common

        name = _gen_mod_name({top_level}, path=mod)
        self.assertEqual(name, ".d.e")

    def test_3(self) -> None:
        common = PurePath(*"abc")
        mod = common
        top_level = PurePath(common, "d")

        name = _gen_mod_name({top_level}, path=mod)
        self.assertEqual(name, "a.b.c")

    def test_4(self) -> None:
        common = PurePath(*"abc")
        mod = common
        top_level = PurePath(common, *"de")

        name = _gen_mod_name({top_level}, path=mod)
        self.assertEqual(name, "a.b.c")

    def test_5(self) -> None:
        common = PurePath(*"abc")
        mod = PurePath(common, "d")
        top_level = PurePath(common, *"ef")

        name = _gen_mod_name({top_level}, path=mod)
        self.assertEqual(name, "a.b.c.d")

    def test_6(self) -> None:
        common = PurePath(*"abc")
        mod = PurePath(common, *"ef")
        top_level = PurePath(common, "d")

        name = _gen_mod_name({top_level}, path=mod)
        self.assertEqual(name, "a.b.c.e.f")

    def test_7(self) -> None:
        common = ""
        mod = PurePath(common, "a")
        top_level = PurePath(common, *"de")

        name = _gen_mod_name({top_level}, path=mod)
        self.assertEqual(name, "a")
