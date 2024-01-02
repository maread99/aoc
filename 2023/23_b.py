"""Day 23: A Long Walk

part a:
See `23_a.py`

part b:
Adapted my initial over-complicated part a solution and it was just never
going to come out for part b. Came back to it a few days later, reframed it
as a graph and got in out within a couple of hours. Executes in under
40s.

Bottom of the leaderboard was 38mins.

#DFS #graph #complex-numbers #grid
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

# establish nodes

NODES = set()
for j, row in enumerate(rows):
    for i in range(len(row) - 2):
        if row[i : i + 3] == ">.>":
            NODES.add(complex(i + 1, j))

cols = ["".join(col) for col in zip(*rows)]

for i, col in enumerate(cols):
    for j in range(len(col) - 2):
        if col[j : j + 3] == "v.v":
            NODES.add(complex(i, j + 1))

# create grid and establish start and end nodes
S: complex | None = None
END: complex | None = None

GRID = {}
for j, row in enumerate(rows):
    for i, c in enumerate(row):
        if j == 0 and c == ".":
            assert S is None
            S = complex(i, j)
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

NOT_NODE = complex(0, 0)
assert NOT_NODE not in NODES

# assert all slopes represented by a node
# for loc, c in GRID.items():
#     assert c != "<"  # there are no slopes to the left
#     assert c != "^"  # there are no slopes pointing upwards
#     if c == ">":
#         assert loc - 1 in NODES or loc + 1 in NODES
#     if c == "v":
#         assert loc - 1j in NODES or loc + 1j in NODES


def map_path(node: complex, d: complex) -> tuple[complex, int]:
    """For a given node and direction, return adjoining node and path length"""
    nloc = node + d
    count = 1
    while nloc not in NODES:
        if GRID[nloc + d] != ".":
            pd = d
            for d in DIRS:
                if d == -pd:  # don't go backwards
                    continue
                if GRID[nloc + d] in (".", ">", "v"):
                    break
            else:
                assert False
        nloc += d
        count += 1
    return nloc, count


NODES.add(S)
NODES.add(END)

# create graph

GRAPH: dict[complex, dict[complex, int]] = defaultdict(dict)
for node in NODES:
    if node == S:
        dest, length = map_path(node, DOWN)
        GRAPH[node][dest] = length
        continue
    if node == END:
        dest, length = map_path(node, UP)
        GRAPH[node][dest] = length
        continue
    if GRID[node + UP] == "v":
        dest, length = map_path(node, UP)
        GRAPH[node][dest] = length
    if GRID[node + DOWN] == "v":
        dest, length = map_path(node, DOWN)
        GRAPH[node][dest] = length
    if GRID[node + LEFT] == ">":
        dest, length = map_path(node, LEFT)
        GRAPH[node][dest] = length
    if GRID[node + RIGHT] == ">":
        dest, length = map_path(node, RIGHT)
        GRAPH[node][dest] = length

# DFS

stack: list[tuple[complex, int, set[complex]]] = [(S, 0, {S})]
MAX_ = 0

while stack:
    node, count, seen = stack.pop()
    if node == END:
        if count > MAX_:
            print(count)
            MAX_ = count
        continue
    for nnode, length in GRAPH[node].items():
        if nnode in seen:
            continue
        stack.append((nnode, count + length, seen | {nnode}))

print(MAX_)
