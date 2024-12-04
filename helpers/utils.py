"""Utilities module for aoc"""

import re


# from https://github.com/mcpower/adventofcode/blob/master/utils.py
def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str) -> list[int]:
    """Return all integers in a string, signed.

    If a '-' divides two integers then the following integer is assumed
    positively signed.

    Examples
    --------
    >>> s = 'sadf fas 444 sas-3as 3 f a 234 as -24 2 f-22sfdas 3-7 qsd11-456bb'
    >>> ints(s)
    [444, -3, 3, 234, -24, 2, -22, 3, 7, 11, 456]
    """
    # from https://github.com/mcpower/adventofcode/blob/master/utils.py
    assert isinstance(s, str), f"you passed in a {type(s)}!!!"
    return lmap(int, re.findall(r"(?:(?<!\d)-)?\d+", s))


def positive_ints(s: str) -> list[int]:
    # from https://github.com/mcpower/adventofcode/blob/master/utils.py
    """Return all integers in a string as positive values.

    Examples
    --------
    >>> s = 'sadf fas 444 sas-3as 3 f a 234 as -24 2 f-22sfdas 3-7 qsd11-456bb'
    >>> positive_ints(s)
    [444, 3, 3, 234, 24, 2, 22, 3, 7, 11, 456]
    """
    assert isinstance(s, str), f"you passed in a {type(s)}!!!"
    return lmap(int, re.findall(r"\d+", s))


# VECTORS

# Complex number vectors

# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
VECS = (
    -1j,  # up
    1 - 1j,  # up right
    1,  # right
    1 + 1j,  # down right
    1j,  # down
    -1 + 1j,  # down left
    -1,  # left
    -1 - 1j,  # up left
)

# Direction vectors
# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRS = (UP, DOWN, LEFT, RIGHT)

UP_L = -1 - 1j
UP_R = 1 - 1j
DOWN_L = -1 + 1j
DOWN_R = 1 + 1j

# Create BOUNDARY around a square grid
assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

BOUNDARY = set()
for i in range(-1, DIM + 1):
    BOUNDARY.add(complex(-1, i))
    BOUNDARY.add(complex(DIM, i))
    BOUNDARY.add(complex(i, -1))
    BOUNDARY.add(complex(i, DIM))
