from pymath.number_theory.primes import *


def test_primes():
    for n1, n2 in zip(primes(10),
                      [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]):
        assert n1 == n2


def test_primes_up_to():
    for n1, n2 in zip(primes_up_to(10),
                      [2, 3, 5, 7]):
        assert n1 == n2
