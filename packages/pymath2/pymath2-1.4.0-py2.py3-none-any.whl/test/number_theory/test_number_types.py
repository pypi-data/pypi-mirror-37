from pymath.number_theory.number_types import *


def test_is_even():
    assert is_even(2) == True
    assert is_even(0) == True
    assert is_even(1) == False
    assert is_even(-1) == False


def test_is_prime():
    assert is_prime(101) == True
    assert is_prime(0) == False
    assert is_prime(1) == False
    assert is_prime(2) == True
    assert is_prime(7) == True
    assert is_prime(-7) == True


def test_is_mersenne_prime():
    assert is_mersenne_prime(3) == True
    assert is_mersenne_prime(4) == False
    assert is_mersenne_prime(11) == False


def test_is_perfect():
    assert is_perfect(6) == True
    assert is_perfect(5) == False
    assert is_perfect(1) == False


def test_is_regular():
    assert is_regular(48) == True
    assert is_regular(75) == True
    assert is_regular(14) == False


def test_is_highly_composite():
    assert is_highly_composite(60) == True
    assert is_highly_composite(59) == False
    assert is_highly_composite(3) == False
    assert is_highly_composite(2) == True
    assert is_highly_composite(1) == True


def test_is_largely_composite():
    assert is_largely_composite(60) == True
    assert is_largely_composite(5) == False
    assert is_largely_composite(3) == True
    assert is_largely_composite(2) == True
    assert is_largely_composite(1) == True
