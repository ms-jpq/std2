from unittest import TestCase

from ..std2.importlib import ld_mod_from_path
from ._consts import TOP_LEVEL


class ModFromPath(TestCase):
    def test_1(self) -> None:
        setup_py = TOP_LEVEL / "__init__.py"

        mod = ld_mod_from_path(setup_py)
        self.assertEqual(mod.__name__, "__init__")
