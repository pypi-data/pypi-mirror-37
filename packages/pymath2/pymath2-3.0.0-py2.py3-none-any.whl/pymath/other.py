from typing import Dict, List, Tuple

__all__ = ['benfords_law', 'convert_base', 'rank']


def convert_base(n: int, b: int) -> List[int]:
    """Returns n converted from base 10 to base b."""
    output = []
    while n >= 1:
        n, r = divmod(n, b)
        output.append(r)
    output.reverse()
    return output


def benfords_law(_list: List[float], first_digit=True) -> \
        Dict[int, Tuple[int, float]]:
    """first_digit determines if we are counting the leftmost digit or the
     rightmost digit"""
    count: Dict[int, int] = {}
    start = 1 if first_digit else 0
    for i in range(start, 10):
        count[i] = 0
    index = 0 if first_digit else -1
    for item in _list:
        count[int(str(item)[index])] += 1
    n = len(_list)
    return {key: (value, value / n) for (key, value) in count.items()}


def rank(_list: List[float], dense=False) -> List[int]:
    rank_dict: Dict[float, int] = {}
    if dense:
        i = 1
        for val in sorted(_list):
            if val not in rank_dict:
                rank_dict[val] = i
                i += 1
    else:
        for i, val in enumerate(sorted(_list)):
            if val not in rank_dict:
                rank_dict[val] = i + 1
    return [rank_dict[i] for i in _list]
