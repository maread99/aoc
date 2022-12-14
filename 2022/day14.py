"""Day 14: Regolith Reservoir

part a: 90mins, too much of which was spent debugging a careless assignment
in the definition of `ROCK`.

part b: 23mins, most of which was time it took to realise the floor needed
to be extended way beyond the prior min/max, not just a bit!
"""

import itertools
import re

from aocd import get_data

raw = get_data(day=14, year=2022)


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", s)))


MIN_X = float("inf")
MAX_X = MAX_Y = 0

ROCK = set()
for line in raw.splitlines():
    for a, b in itertools.pairwise(line.split(" -> ")):
        (x1, y1), (x2, y2) = ints(a), ints(b)
        if x1 - x2:
            ROCK |= {(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)}
        else:
            ROCK |= {(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)}

        MIN_X, MAX_X = min(MIN_X, x1, x2), max(MAX_X, x1, x2)
        MAX_Y = max(MAX_Y, y1, y2)


def get_rock():
    return ROCK.copy()


def is_in_bounds(s: tuple[int, int]):
    return MIN_X <= s[0] <= MAX_X and s[1] < MAX_Y  # the x bound check is superfluous!


solid = get_rock()


def drop_sand(start: tuple[int, int]) -> bool:
    s = ns = start
    while ns not in solid:
        if not is_in_bounds(ns):
            return False
        s = ns
        ns = (s[0], s[1] + 1)
    if (ns := (s[0] - 1, s[1] + 1)) not in solid:
        return drop_sand(ns)
    if (ns := (s[0] + 1, s[1] + 1)) not in solid:
        return drop_sand(ns)
    solid.add(s)
    return True


t = 0
S = (500, 0)
while drop_sand(S):
    t += 1
    continue
print(t)

# part b

solid = get_rock()
solid |= {(x, MAX_Y + 2) for x in range(MIN_X - 5000, MAX_X + 5000)}
t = 0


# as above with is_in_bounds check removed and set to return False if sand added at S.
def drop_sand(start: tuple[int, int]) -> bool:
    s = ns = start
    while ns not in solid:
        s = ns
        ns = (s[0], s[1] + 1)
    if (ns := (s[0] - 1, s[1] + 1)) not in solid:
        return drop_sand(ns)
    if (ns := (s[0] + 1, s[1] + 1)) not in solid:
        return drop_sand(ns)
    solid.add(s)
    return s != S


t = 0
while drop_sand(S):
    t += 1
    continue
print(t)
