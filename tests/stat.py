from stat import filemode
from unittest import TestCase

from ..std2.stat import RW_R__R__, RWXR_XR_X


class RWX(TestCase):
    def test_1(self) -> None:
        mode = filemode(RWXR_XR_X)
        self.assertEqual(mode, "?rwxr-xr-x")

    def test_2(self) -> None:
        mode = filemode(RW_R__R__)
        self.assertEqual(mode, "?rw-r--r--")
