from dataclasses import dataclass
from typing import List, MutableSequence, Optional, Sequence, Tuple
from unittest import TestCase

from ..std2.collections import defaultlist

_SMS = Sequence[MutableSequence[str]]

_Into = Tuple[Optional[int], Optional[int], Optional[int], Sequence[str]]


@dataclass(frozen=True)
class _TestCase:
    expected: List[str]
    into: Sequence[_Into]
    debug: bool = False


class DefaultList(TestCase):
    def test_1(self) -> None:
        l2: Sequence[str] = []
        ls: _SMS = (defaultlist(lambda: ""), [])
        for l1 in ls:
            self.assertEqual(len(l1), 0)
            with self.assertRaises(IndexError):
                l1[1]
            with self.assertRaises(IndexError):
                l1[-1]
            self.assertEqual(l1[:], l2)

    def test_2(self) -> None:
        ls: _SMS = (defaultlist(lambda: ""), [])
        l2 = ["a"]
        for l1 in ls:
            l1.append("a")
            self.assertIn("a", l1)
            self.assertEqual(len(l1), 1)
            with self.assertRaises(IndexError):
                l1[1]
            with self.assertRaises(IndexError):
                l1[-2]
            self.assertEqual(l1[0], "a")
            self.assertEqual(l1[-1], "a")
            self.assertEqual(l1[:], l2)

    def test_3(self) -> None:
        ls: _SMS = (defaultlist(lambda: ""), [])
        l2 = ["a"]
        for l1 in ls:
            l1.insert(2, "a")
            self.assertEqual(len(l1), 1)
            with self.assertRaises(IndexError):
                l1[1]
            with self.assertRaises(IndexError):
                l1[-2]
            self.assertEqual(l1[:], l2)

    def test_4(self) -> None:
        ls: _SMS = (defaultlist(lambda: ""), [])
        l2 = ["b", "d", "c", "a"]
        for l1 in ls:
            l1.insert(2, "a")
            l1.insert(0, "b")
            l1.insert(-1, "c")
            l1.insert(1, "d")
            self.assertEqual(len(l1), len(l2))
            self.assertEqual(l1[:], l2)

    def test_5(self) -> None:
        for case in (
            _TestCase(into=((None, None, None, ()),), expected=[]),
            _TestCase(
                into=((None, None, None, ("a", "b", "c")),),
                expected=["a", "b", "c"],
            ),
            _TestCase(
                into=(
                    (None, None, None, ("a", "b", "c")),
                    (None, None, None, ("a", "b", "c")),
                ),
                expected=["a", "b", "c"],
            ),
            _TestCase(
                into=(
                    (None, None, None, ("e", "f")),
                    (None, None, None, ("a", "b", "c")),
                ),
                expected=["a", "b", "c"],
            ),
            _TestCase(
                into=(
                    (None, None, None, ("e", "f", "g", "h")),
                    (None, None, None, ("a", "b", "c")),
                ),
                expected=["a", "b", "c"],
            ),
            _TestCase(
                into=(
                    (None, None, None, ("e", "f", "g", "h")),
                    (0, 4, None, ("a", "b", "c")),
                ),
                expected=["a", "b", "c"],
            ),
            _TestCase(
                into=(
                    (None, None, None, ("e", "f", "g", "h")),
                    (0, 4, 1, ("a", "b", "c")),
                ),
                expected=["a", "b", "c"],
            ),
            _TestCase(
                into=(
                    (None, None, None, ("e", "f", "g", "h")),
                    (0, 99, None, ("a", "b", "c")),
                ),
                expected=["a", "b", "c"],
            ),
            _TestCase(
                into=(
                    (None, None, None, ("e", "f", "g", "h")),
                    (0, 99, 1, ("a", "b", "c")),
                ),
                expected=["a", "b", "c"],
            ),
            # _TestCase(
            #     into=(
            #         (None, None, None, ("e", "f", "g", "h", "i")),
            #         (0, 2, None, ("a", "b", "c")),
            #     ),
            #     expected=["a", "b", "c", "g", "h", "i"],
            #     debug=True,
            # ),
        ):
            l1 = defaultlist(lambda: "")
            if case.debug:
                l1._debug = True
            l2: MutableSequence[str] = []
            for i, j, k, into in case.into:
                l2[i:j:k] = into
                l1[i:j:k] = into

            self.assertEqual(l2[:], case.expected, case)
            self.assertEqual(l1[:], case.expected, case)
