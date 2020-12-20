from os.path import join
from unittest import TestCase

from ..std2.importlib import _gen_mod_name, module_from_path
from ._consts import TOP_LEVEL


class ModFromPath(TestCase):
    def test_1(self) -> None:
        setup_py = join(TOP_LEVEL, "setup.py")
        mod = module_from_path(setup_py, top_level=TOP_LEVEL)
        self.assertEqual(mod.__name__, ".setup")

    def test_2(self) -> None:
        common = join(*"abc")
        mod = join(common, *"de")
        top_level = common
        name = _gen_mod_name(mod, top_level=top_level)
        self.assertEqual(name, ".d.e")

    def test_3(self) -> None:
        common = join(*"abc")
        mod = common
        top_level = join(common, "d")
        name = _gen_mod_name(mod, top_level=top_level)
        self.assertEqual(name, "..c")

    def test_4(self) -> None:
        common = join(*"abc")
        mod = join(common, "d")
        top_level = join(common, *"ef")
        name = _gen_mod_name(mod, top_level=top_level)
        self.assertEqual(name, "...d")

    def test_5(self) -> None:
        common = join(*"abc")
        mod = join(common, *"ef")
        top_level = join(common, "d")
        name = _gen_mod_name(mod, top_level=top_level)
        self.assertEqual(name, "..e.f")
