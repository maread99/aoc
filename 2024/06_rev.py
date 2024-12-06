"""Day 6: Guard Gallivant

This revised version introduces a further optimisation that realises the
only circumstances worth considering are the first occassions that the
guard enters a new location, i.e. the first occassions that the guard can
encounter a new obstacle. This reduced the execution time from 8 seconds to
3 seconds ... not worth the extra code for this puzzle, but the right way
to think about such puzzles and an approach that could offer more
meaningful timesavings on others.

I picked up on this optimisation from @gahjelle:
    https://github.com/gahjelle/advent_of_code/blob/main/python/2024/06_guard_gallivant/aoc202406.py

#sets #complex-numbers
"""

from collections import deque
from aocd import get_data


raw = get_data(day=6, year=2024)

# raw = """....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# """

rows = raw.splitlines()

OBS = set()
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        if c == "^":
            START = complex(i, j)
        elif c == "#":
            OBS.add(complex(i, j))


# Create BOUNDARY around a square grid
assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

BOUNDARY = set()
for i in range(-1, DIM + 1):
    BOUNDARY.add(complex(-1, i))
    BOUNDARY.add(complex(DIM, i))
    BOUNDARY.add(complex(i, -1))
    BOUNDARY.add(complex(i, DIM))


UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRS = (UP, RIGHT, DOWN, LEFT)


dirs = deque(DIRS)
loc = START
seen = {loc}
path = [(loc, dirs[0])]
while True:
    loc_new = loc + dirs[0]
    while loc_new in OBS:
        dirs.rotate(-1)
        loc_new = loc + dirs[0]
    if loc_new in BOUNDARY:
        break
    loc = loc_new
    if loc not in seen:
        path.append((loc, dirs[0]))
    seen.add(loc)
print(len(seen))


def is_loop(path: list[tuple[complex, complex]]) -> bool:
    ob, drct = path[-1]
    seen = set(path[:-1])
    obs = OBS | {ob}
    loc = ob - drct
    dirs = deque(DIRS)
    while dirs[0] != drct:
        dirs.rotate(-1)
    while True:
        loc_new = loc + dirs[0]
        while loc_new in obs:
            dirs.rotate(-1)
            loc_new = loc + dirs[0]
        if loc_new in BOUNDARY:
            return False
        loc = loc_new
        if (loc, dirs[0]) in seen:
            return True
        seen.add((loc, dirs[0]))


total = 0
for i in range(len(path)):
    p = path[: i + 1]
    if p[-1][0] == START:
        continue
    total += is_loop(p)
print(total)
