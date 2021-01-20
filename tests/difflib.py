from itertools import islice
from random import randint
from typing import Iterator, MutableSequence, Tuple
from unittest import TestCase

from ..std2.difflib import trans_inplace
from ._consts import BIG_REP_FACTOR


def _rand_gen(
    lo: int, hi: int
) -> Iterator[Tuple[MutableSequence[int], MutableSequence[int]]]:
    gen = iter(lambda: randint(lo, hi), None)
    while True:
        yield [*islice(gen, randint(lo, hi))], [*islice(gen, randint(lo, hi))]


class TransInplace(TestCase):
    def test_1(self) -> None:
        gen = _rand_gen(1, BIG_REP_FACTOR)
        for _ in range(BIG_REP_FACTOR):
            seq1, seq2 = next(gen)
            for (lo, hi), replace in trans_inplace(seq1, seq2, unifying=3):
                seq1[lo:hi] = replace

            self.assertEqual(seq1, seq2)
