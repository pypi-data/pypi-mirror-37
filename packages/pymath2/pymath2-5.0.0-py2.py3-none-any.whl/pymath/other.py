import string
from typing import Dict, List, Tuple

__all__ = ['benfords_law', 'convert_base', 'convert_to_base_10', 'rank']


def convert_to_base_10(x: int, base: int) -> str:
    """https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-in-any-base-to-a-string"""
    digits = string.digits + string.ascii_uppercase
    if x < 0:
        sign = -1
    elif x == 0:
        return digits[0]
    else:
        sign = 1
    x *= sign
    converted = []
    while x:
        converted.append(digits[int(x % base)])
        x = int(x // base)
    if sign < 0:
        converted.append('-')
    converted.reverse()
    return ''.join(converted)


def convert_base(x: str, source: int, dest: int) -> str:
    """
    Returns:
        'n' converted from base 'source' to base 'dest'
    """
    if source == 10:
        return convert_to_base_10(int(x), dest)
    return convert_to_base_10(int(x, source), dest)


def benfords_law(_list: List[float], first_digit=True) -> \
        Dict[int, Tuple[int, float]]:
    """
    Args:
        first_digit: determines if we are counting the leftmost or rightmost
        digit
    """
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
