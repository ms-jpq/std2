from typing import Dict, FrozenSet, List, Mapping, Sequence, Set
from unittest import TestCase

from ..std2.types import Void, VoidType, freeze, or_else


class VoidTest(TestCase):
    def test_1(self) -> None:
        self.assertIs(Void, Void)

    def test_2(self) -> None:
        self.assertIsNot(Void, VoidType)

    def test_3(self) -> None:
        self.assertIsNot(Void, VoidType())

    def test_4(self) -> None:
        thing: None = or_else(Void, None)
        self.assertEqual(thing, None)


class Freeze(TestCase):
    def test_1(self) -> None:
        l1: List[int] = []
        d1: Dict[int, int] = {}
        s1: Set[int] = set()

        l2: Sequence[int] = freeze(l1)
        d2: Mapping[int, int] = freeze(d1)
        s2: FrozenSet[int] = freeze(s1)
