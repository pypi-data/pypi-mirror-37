from functools import reduce
from math import factorial
from typing import Collection, Iterator, List, TypeVar

__all__ = ['C', 'P', 'powerset']

T = TypeVar('T')


def C(n: int, *k: int) -> int:
    if len(k) == 1:
        return factorial(n) // (factorial(n - k[0]) * factorial(k[0]))
    return factorial(n) // reduce(lambda x, y: x * y,
                                  map(lambda x: factorial(x), k))


def P(n: int, k: int) -> int:
    return factorial(n) // (factorial(n - k))


def powerset(collection: Collection[T]) -> List[List[T]]:
    def powerset_recur(seq: List[T]) -> Iterator[List[T]]:
        if len(seq) == 0:
            yield []
        else:
            for item in powerset_recur(seq[1:]):
                yield item
                yield [seq[0]] + item

    return list(powerset_recur(list(collection)))
