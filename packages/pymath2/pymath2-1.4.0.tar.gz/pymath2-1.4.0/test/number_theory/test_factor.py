from pymath.number_theory.factor import *


def test_factors():
    for n1, n2 in zip(factors(50),
                      [1, 2, 5, 10, 25, 50]):
        assert n1 == n2
    for _ in factors(0):
        assert False
    for n1, n2 in zip(factors(-50),
                      [1, 2, 5, 10, 25, 50]):
        assert n1 == n2


def test_lcm():
    assert lcm(60, 18) == 180
    assert lcm(60, 18, 3) == 180


def test_gcd():
    assert gcd(60, 18) == 6
    assert gcd(60, 18, 3) == 3


def test_extended_lcm():
    assert extended_lcm(5, 2) == [10, 2, 5]
    assert extended_lcm(5, 2, 3) == [30, 6, 15, 10]


def test_extended_gcd():
    assert extended_gcd(10, 6) == (2, -1, 2)


def test_prime_factors():
    for n1, n2 in zip(prime_factors(5), [5]):
        assert n1 == n2
    for n1, n2 in zip(prime_factors(60), [2, 2, 3, 5]):
        assert n1 == n2


def test_largest_prime_factor():
    assert largest_prime_factor(60) == 5
    assert largest_prime_factor(11) == 11


def test_coprime():
    assert are_coprime(5, 2) == True
    assert are_coprime(2, 2) == False
    assert are_coprime(2, 1) == True
    assert are_coprime(2, 0) == False
    assert are_coprime(0, 0) == False
    assert are_coprime(10, 2, 4) == False
    assert are_coprime(10, 3, 4) == True


def test_phi():
    assert phi(1) == 1
    assert phi(2) == 1
    assert phi(3) == 2
    assert phi(10) == 4
    assert phi(16) == 8


def test_coprimes():
    for n1, n2 in zip(coprimes(1), [1]):
        assert n1 == n2
    for n1, n2 in zip(coprimes(10), [1, 3, 7, 9]):
        assert n1 == n2
    for n1, n2 in zip(coprimes(16), [1, 3, 5, 7, 9, 11, 13, 15]):
        assert n1 == n2
