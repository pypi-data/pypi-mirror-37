from math import log, sqrt

from . import factor

__all__ = [
    'is_composite', 'is_even', 'is_highly_composite', 'is_largely_composite',
    'is_mersenne_prime', 'is_odd', 'is_perfect', 'is_prime', 'is_regular'
]


def is_even(n: int) -> bool:
    return n % 2 == 0


def is_odd(n: int) -> bool:
    return not is_even(n)


def is_prime(n: int) -> bool:
    n = abs(n)
    return n > 1 and all((n % i) for i in range(2, 2 + int(sqrt(n) - 1)))


def is_composite(n: int) -> bool:
    return not is_prime(n)


def is_mersenne_prime(n: int) -> int:
    return log(n + 1, 2).is_integer() and is_prime(n)


def is_perfect(n: int) -> bool:
    return sum(list(factor.factors(n))) == 2 * n


def is_regular(n: int) -> bool:
    return all(p in [2, 3, 5] for p in factor.prime_factors(n))


def is_highly_composite(n: int) -> bool:
    num_factors = len(list(factor.factors(n)))
    for i in range(n):
        if len(list(factor.factors(i))) >= num_factors:
            return False
    return True


def is_largely_composite(n: int) -> bool:
    num_factors = len(list(factor.factors(n)))
    for i in range(n):
        if len(list(factor.factors(i))) > num_factors:
            return False
    return True
