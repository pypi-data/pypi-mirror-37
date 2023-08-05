from pymath.other import *


def test_convert_base():
    assert convert_base(5, 2) == [1, 0, 1]
    assert convert_base(7, 4) == [1, 3]


def test_benfords_law():
    assert benfords_law(range(1, 11)) == {
        1: (2, 0.2), 2: (1, 0.1), 3: (1, 0.1), 4: (1, 0.1),
        5: (1, 0.1), 6: (1, 0.1), 7: (1, 0.1), 8: (1, 0.1), 9: (1, 0.1)
    }


def test_rank():
    assert rank([1, 4, 4, 20, 15, 6]) == [1, 2, 2, 6, 5, 4]
    assert rank([1, 4, 4, 20, 15, 6], dense=True) == [1, 2, 2, 5, 4, 3]
