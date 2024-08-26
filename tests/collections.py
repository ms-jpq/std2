from collections import defaultdict
from typing import MutableMapping, Sequence, cast
from unittest import TestCase

from ..std2.collections import defaultlist


class DefaultList(TestCase):
    def test_5(self) -> None:
        for d0, l2 in (
            ({}, cast(Sequence[str], [])),
            ({0: "a"}, ["a"]),
            ({1: "a"}, ["", "a"]),
            ({2: "a"}, ["", "", "a"]),
            ({2: "a", 4: "b"}, ["", "", "a", "", "b"]),
        ):
            d1: MutableMapping[int, str] = defaultdict(lambda: "")
            d1.update(d0)
            l1 = defaultlist(d1)

            self.assertEqual(l1[:], l2)
