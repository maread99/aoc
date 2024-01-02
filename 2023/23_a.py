"""Day 23: A Long Walk

part a: 2hrs
Initially solved with a very over-complicated BFS. Subsequently tidied and
changed to DFS to reduce execution time (version here).

part b:
See `23_b.py`

#DFS #complex-numbers #grid
"""

from collections import defaultdict

from aocd import get_data

raw = get_data(day=23, year=2023)

# raw = """#.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#
# """

rows = raw.splitlines()

S: complex | None = None
END: complex | None = None

GRID = {}
for j, row in enumerate(rows):
    for i, c in enumerate(row):
        if j == 0 and c == ".":
            assert S is None
            S = complex(i, 1)  # move down already and block the path back
            c = "#"
        if j == len(rows) - 1 and c == ".":
            assert END is None
            END = complex(i, j)
        GRID[complex(i, j)] = c

assert S is not None and END is not None

# Direction vectors
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRS = (UP, DOWN, LEFT, RIGHT)

SLOPE_MAP = {
    ">": RIGHT,
    "<": LEFT,
    "^": UP,
    "v": DOWN,
}

# GLOBAL_SEEN not really worth it, just executes in ms rather than a few seconds
GLOBAL_SEEN: dict[complex, int] = defaultdict(int)
MAX_ = 0

stack: list[tuple[complex, int, set[complex]]] = [(S, 1, set())]  # tuple of loc, steps

while stack:
    loc, s, seen = stack.pop()
    if loc in GLOBAL_SEEN and s <= GLOBAL_SEEN[loc]:
        continue
    GLOBAL_SEEN[loc] = s

    for d in DIRS:
        nloc = loc + d
        if nloc == END:
            MAX_ = max(MAX_, s + 1)
            continue
        if nloc in seen:
            continue
        c = GRID[nloc]
        if c == "#":
            continue
        elif c == ".":
            pass
        elif d != SLOPE_MAP[c]:
            continue
        seen.add(nloc)
        stack.append((nloc, s + 1, seen.copy()))

print(MAX_)
