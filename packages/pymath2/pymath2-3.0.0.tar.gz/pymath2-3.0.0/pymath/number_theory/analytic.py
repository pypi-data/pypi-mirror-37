from typing import Optional, Tuple

from . import number_types, primes

__all__ = ['goldbach', 'goldbach_triple']


def goldbach(n: int) -> Optional[Tuple[int, int]]:
    if n <= 2 or number_types.is_odd(n):
        return None
    _primes = list(primes.primes_up_to(n))
    for p1 in _primes:
        for p2 in reversed(_primes):
            if p1 + p2 == n:
                return p1, p2
            if p1 + p2 < n:
                break
    return None


def goldbach_triple(n: int) -> Optional[Tuple[int, int, int]]:
    if n <= 5:
        return None
    _primes = list(primes.primes_up_to(n))
    for p1 in _primes:
        for p2 in _primes:
            for p3 in _primes:
                if p1 + p2 + p3 == n:
                    return p1, p2, p3
                if p1 + p2 + p3 > n:
                    break
    return None
