from pymath.number_theory.analytic import *


def test_goldbach():
    assert goldbach(1) == None
    assert goldbach(11) == None
    assert goldbach(4) == (2, 2)
    assert goldbach(72) == (5, 67)
    assert goldbach(16) == (3, 13)


def test_goldbach_triple():
    assert goldbach_triple(5) == None
    assert goldbach_triple(10) == (2, 3, 5)
    assert goldbach_triple(500) == (2, 7, 491)
    assert goldbach_triple(71) == (2, 2, 67)
