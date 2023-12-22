"""Day 21: Step Counter

part a: 1hr 20min
Wasted 15min trying to implement as a DFS which, literally, couldn't get
out of dead ends. Then took a while to figure out that only want to record
the end plots on even counts. Effectively all seen cells can be either
an end plot on an odd step or an even step, but not both (I think?).

part b: Didn't get it out after umpteen hours.
See `21_b_X.py`

total: Didn't get out part b. (bottom of the leaderboard was 1hr 19)

#BFS
"""

from collections import deque

from aocd import get_data


raw = get_data(day=21, year=2023)

# raw = """...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# """

rows = raw.splitlines()

GRID = {}
for j, row in enumerate(rows):
    for i, c in enumerate(row):
        if c == "S":
            S = complex(i, j)
            c = "."
        GRID[complex(i, j)] = c

# Add BOUNDARY around square grid
assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

for i in range(-1, DIM + 1):
    GRID[complex(-1, i)] = "#"
    GRID[complex(DIM, i)] = "#"
    GRID[complex(i, -1)] = "#"
    GRID[complex(i, DIM)] = "#"

# Direction vectors
# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRS = (UP, DOWN, LEFT, RIGHT)


queue = deque([(S, 0)])  # tuples of (loc, count)
STEPS = 64
seen = set()
end_plots = set()
while queue:
    loc, i = queue.popleft()
    if i == STEPS:
        continue
    for d in DIRS:
        nloc = loc + d
        if nloc in seen:
            continue
        if GRID[nloc] == "#":
            continue
        queue.append((nloc, i + 1))
        seen.add(nloc)
        if not ((i + 1) % 2):
            end_plots.add(nloc)


print(len(end_plots))
