from collections import defaultdict
from itertools import islice
from math import log
from typing import Dict, Iterator, List, Optional

__all__ = [
    'primes_iter', 'primes', 'primes_up_to_iter', 'primes_up_to',
    'mersenne_primes_iter', 'mersenne_primes', 'mersenne_primes_up_to_iter',
    'mersenne_primes_up_to',
]


def yield_values_up_to(n: int, _iter: Iterator[int]):
    num = next(_iter)
    while num <= n:
        yield n
        num = next(_iter)


def primes_iter(n: Optional[int] = None) -> Iterator[int]:
    def infinite_primes() -> Iterator[int]:
        D: Dict[int, List[int]] = defaultdict(list)
        q = 2
        while True:
            if q not in D:
                yield q
                D[q * q] = [q]
            else:
                for p in D[q]:
                    D[p + q].append(p)
                del D[q]
            q += 1

    if n is None:
        return infinite_primes()
    return islice(infinite_primes(), n)


def primes(n: Optional[int] = None) -> List[int]:
    return list(primes_iter(n))


def primes_up_to_iter(n: int) -> Iterator[int]:
    return yield_values_up_to(n, primes_iter())


def primes_up_to(n: int) -> List[int]:
    return list(primes_up_to_iter(n))


def mersenne_primes_iter(n: Optional[int] = None) -> Iterator[int]:
    def infinite_mersenne_primes() -> Iterator[int]:
        D: Dict[int, List[int]] = defaultdict(list)
        q = 2
        while True:
            if q not in D:
                if log(q + 1, 2).is_integer():
                    yield q
                D[q * q] = [q]
            else:
                for p in D[q]:
                    D[p + q].append(p)
                del D[q]
            q += 1

    if n is None:
        return infinite_mersenne_primes()
    return islice(infinite_mersenne_primes(), n)


def mersenne_primes(n: Optional[int] = None) -> List[int]:
    return list(mersenne_primes_iter(n))


def mersenne_primes_up_to_iter(n: int) -> Iterator[int]:
    return yield_values_up_to(n, mersenne_primes_iter())


def mersenne_primes_up_to(n: int) -> List[int]:
    return list(mersenne_primes_iter(n))
