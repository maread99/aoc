"""Day 6: Guard Gallivant

part a: 26mins
Initially evaluated the number of 'steps' that the guard took rather than
the number of distinct locations he visited. Only after debugging for a
while did I read the question properly!

part b: 13mins
Did understand the question, although still decided to evaluate from how
many starting positions the guard would enter a loop rather than the number
of locations at which adding an obstacle will create a loop (with the
guard's starting location unchanged). Didn't take too long to realise the
error.
My original solution looped through placing an obstacle in ALL free spaces
and took 37 seconds to execute. The solution below adds a conditional
statement (as commented) to not bother with locations that are not on the
guard's original route (i.e. locations which the guard would never
encounter). This brought the execution time down to 8 seconds.

total: 39mins, 4.4x bottom of the leaderboard.

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
seen_a = {START}
while True:
    loc_new = loc + dirs[0]
    while loc_new in OBS:
        dirs.rotate(-1)
        loc_new = loc + dirs[0]
    if loc_new in BOUNDARY:
        break
    loc = loc_new
    seen_a.add(loc)
print(len(seen_a))


def is_loop(ob: complex) -> bool:
    obs = OBS | {ob}
    dirs = deque(DIRS)
    loc = START
    seen = {(loc, dirs[0])}
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
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        if c in ("^", "#"):
            continue
        # added condition to ignore locations that guard would not encounter
        if complex(i, j) not in seen_a:
            continue
        total += is_loop(complex(i, j))
print(total)
