from pymath.counting import *


def test_C():
    assert C(5, 2) == 10
    assert C(7, 4) == 35


def test_P():
    assert P(5, 2) == 20
    assert P(7, 4) == 840


def test_powerset():
    for e1, e2 in zip(powerset([1, 2]),
                      [[], [1], [2], [1, 2]]):
        assert e1 == e2
