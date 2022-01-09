from stat import filemode
from unittest import TestCase

from ..std2.stat import RW_R__R__, RWXR_XR_X


class HR(TestCase):
    def test_1(self) -> None:
        mode = filemode(RWXR_XR_X)
        self.assertEquals(mode, "?rwxr-xr-x")

    def test_2(self) -> None:
        mode = filemode(RW_R__R__)
        self.assertEquals(mode, "?rw-r--r--")
