"""Day 17: Clumsy Crucible

part a: 3hrs 7 mins
Had to debug various issues. Some related to failing to READ THE QUESTION.
Another was a stupid bug in the state key.

part b: Say 2hrs 30mins
Initial implementation for part 1 took 11 mins to execute. Spent a good
amount of time getting it down to under 2mins. Using the same basis for the
part 2 implementation got it out in about 8 minutes.

total: Say 5hrs 40mins. 17x bottom of the leaderboard.

Having subsequently looked around, the Dijkstra's algorithm is the one to
have used here, employing a priority queue (i.e. heap). See 17_rev.py.

#BFS  #optimization
"""
import math
from collections import deque

from aocd import get_data

raw = get_data(day=17, year=2023)

raw = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

# Direction vectors
# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

rows = raw.splitlines()

GRID = {}
# create grid
for j, row in enumerate(rows):
    for i, c in enumerate(row):
        GRID[complex(i, j)] = int(c)

assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

END = complex(DIM - 1, DIM - 1)

# part a

queue = deque(
    [
        (complex(1, 0), GRID[complex(1, 0)], (RIGHT, 1)),
        (complex(0, 1), GRID[complex(0, 1)], (DOWN, 1)),
    ]
)  # tuples of loc, accumulated heat, (prior direcion, count of prior direction)

# key as tuple(loc, tuple(previous dir, previous direction count))
min_heats: dict[tuple[complex, tuple[complex, int]], int] = {}

min_ = math.inf

while queue:
    loc, heat, (pd, pd_count) = queue.popleft()

    for d in DIRECTIONS:
        if d == -pd:
            continue

        if d == pd:
            if pd_count == 3:
                continue
            else:
                npd_count = pd_count + 1
        else:
            npd_count = 1

        nloc = loc + d
        if nloc.real < 0 or nloc.real >= DIM or nloc.imag < 0 or nloc.imag >= DIM:
            continue  # out of bounds

        nheat = heat + GRID[nloc]

        key = (nloc, (d, npd_count))
        if heat >= min_heats.get(key, math.inf):
            continue
        min_heats[key] = heat

        if loc == END:
            min_ = min(min_, heat)
            continue

        queue.append((nloc, nheat, (d, npd_count)))

print(min_)

# part b

queue = deque(
    [
        (complex(4, 0), sum(GRID[complex(i, 0)] for i in range(1, 5)), (RIGHT, 4)),
        (complex(0, 4), sum(GRID[complex(0, i)] for i in range(1, 5)), (DOWN, 4)),
    ]
)  # as for part a

min_heats: dict[tuple[complex, tuple[complex, int]], int] = {}  # as for part a

min_ = math.inf

# part b

while queue:
    loc, heat, (pd, pd_count) = queue.popleft()

    for d in DIRECTIONS:
        if d == -pd:
            continue
        if d == pd:
            if pd_count == 10:
                continue
            else:
                npd_count = pd_count + 1
        else:
            npd_count = 4

        nloc = loc + (d * (1 if d == pd else 4))
        if nloc.real < 0 or nloc.real >= DIM or nloc.imag < 0 or nloc.imag >= DIM:
            continue  # out of bounds

        if d == pd:
            nheat = heat + GRID[nloc]
        else:
            nheat = heat + sum(GRID[loc + (d * i)] for i in range(1, 5))

        key = (nloc, (d, npd_count))
        if heat >= min_heats.get(key, math.inf):
            continue
        min_heats[key] = heat

        if loc == END:
            min_ = min(min_, heat)
            continue

        queue.append((nloc, nheat, (d, npd_count)))

print(min_)
