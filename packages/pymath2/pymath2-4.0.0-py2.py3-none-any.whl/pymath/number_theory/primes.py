from collections import defaultdict
from itertools import islice, takewhile
from math import log
from typing import Dict, Iterator, List, Optional

__all__ = [
    'primes_generator', 'primes', 'primes_up_to_generator', 'primes_up_to',
    'mersenne_primes_generator', 'mersenne_primes',
    'mersenne_primes_up_to_generator', 'mersenne_primes_up_to',
]


def primes_generator(n: Optional[int] = None) -> Iterator[int]:
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
    return list(primes_generator(n))


def primes_up_to_generator(n: int) -> Iterator[int]:
    return takewhile(lambda x: x <= n, primes_generator())


def primes_up_to(n: int) -> List[int]:
    return list(primes_up_to_generator(n))


def mersenne_primes_generator(n: Optional[int] = None) -> Iterator[int]:
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
    return list(mersenne_primes_generator(n))


def mersenne_primes_up_to_generator(n: int) -> Iterator[int]:
    return takewhile(lambda x: x <= n, mersenne_primes_generator())


def mersenne_primes_up_to(n: int) -> List[int]:
    return list(mersenne_primes_generator(n))
