"""Day 4: Printing Department

part 1: 28mins
Rusty on working with grids - ummed and ahhed over the best way to do it.
Considered using a dictionary to hold the grid data and complex numbers to
navigate although felt that might be overkill. Happy with having just
iterated over the string data.

part 2: 13mins

total: 41mins
17113
#sets  #grid
"""

from aocd import get_data

# raw = get_data(day=4, year=2025)

raw = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UP_L = (-1, -1)
UP_R = (1, -1)
DOWN_L = (-1, 1)
DOWN_R = (1, 1)
VECS = (UP, DOWN, LEFT, RIGHT, UP_L, UP_R, DOWN_L, DOWN_R)

ROWS = raw.splitlines()

assert len(ROWS) == len(ROWS[0]), (len(ROWS), len(ROWS[0]), ROWS)  # assert square
DIM = len(ROWS)

# set EMPTY to boundary positions to avoid considering cells outside of grid
EMPTY = set()
for i in range(-1, DIM + 1):
    EMPTY.add((-1, i))
    EMPTY.add((DIM, i))
    EMPTY.add((i, -1))
    EMPTY.add((i, DIM))

# ... and add all cells within grid where there is no paper
for j in range(len(ROWS[0])):
    for i in range(len(ROWS)):
        if ROWS[j][i] != "@":
            EMPTY.add((i, j))


def get_can_remove() -> set[tuple[int, int]]:
    """Return set of positions of paper rolls that can remove."""
    can_remove = set()
    for j in range(len(ROWS[0])):
        for i in range(len(ROWS)):
            p = (i, j)
            if p in EMPTY:
                continue
            # count how many adjacent positions are not empty
            count = 0
            for v in VECS:
                ap = (i + v[0], j + v[1])
                if ap not in EMPTY:
                    count += 1
                if count > 3:
                    break
            if count < 4:
                can_remove.add(p)
    return can_remove


# part 1
print(len(get_can_remove()))

# part 2
removed = 0
while can_remove := get_can_remove():
    removed += len(can_remove)
    EMPTY |= can_remove
print(removed)
