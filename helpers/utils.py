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
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
VECS = (UP, DOWN, LEFT, RIGHT)

UP_L = (-1, -1)
UP_R = (1, -1)
DOWN_L = (-1, 1)
DOWN_R = (1, 1)

VECS = (UP, DOWN, LEFT, RIGHT, UP_L, UP_R, DOWN_L, DOWN_R)


# Direction vectors as complex numbers
# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
VECS = (UP, DOWN, LEFT, RIGHT)

UP_L = -1 - 1j
UP_R = 1 - 1j
DOWN_L = -1 + 1j
DOWN_R = 1 + 1j
VECS = (UP, DOWN, LEFT, RIGHT, UP_L, UP_R, DOWN_L, DOWN_R)


# Create BOUNDARY around a square grid
assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

BOUNDARY = set()
for i in range(-1, DIM + 1):
    BOUNDARY.add(complex(-1, i))
    BOUNDARY.add(complex(DIM, i))
    BOUNDARY.add(complex(i, -1))
    BOUNDARY.add(complex(i, DIM))

# Empty grid
grid = [["."] * len(rows[0]) for _ in range(len(rows))]

# print a grid
print("\n".join(["".join(l) for l in grid]))


# BFS
START = (0, 0)  # as required
queue = deque([(START, 0)])
obs = set()  # as required
seen = set()
while queue:
    loc, n = queue.popleft()
    for v in VECS4:
        # nloc = loc + v  # if using complex numbers
        nloc = (loc[0] + v[0], loc[1] + v[1])
        if nloc in obs:
            continue
        if nloc in seen:
            continue
        if nloc == END:
            n += 1
            break_ = True
            break
        seen.add(nloc)
        queue.append((nloc, n + 1))
    if break_:
        break
print(n)


# PATTERN IDENTIFICATION
def find_pattern(vals: list) -> list:
    """find the longest repeating pattern in `vals`."""
    for lgn in reversed(range(1, len(vals) // 2)):
        n = 1
        while lgn * (n + 1) < len(vals):
            if vals[:lgn] != vals[lgn * n : lgn * (n + 1)]:
                break
            n += 1
        else:
            # verify that any 'part' at the end also matches...
            vals_end = vals[-(len(vals) % lgn * (n + 2)) :]
            if vals_end == vals[: len(vals_end)]:
                return vals[:lgn]
    return []
