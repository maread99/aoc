"""Day 23: A Long Walk

This alternative implements the DFS via recursion as opposed to a stack.
(Aside from this last part it's otherwise unchanged from `23_b.py`.)
Although not much quicker than `23_b.py`, has the advantage of faciliating
the use of a single global `seen`. Nodes can be added to `seen` ahead of
moving down a branch (so as not to move back to the same node) and then
removed before moving on to other branches (in order that those other
branches can traverse the freed-up node from other directions).

Written after seeing:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day23p2.py

#DFS #graph #complex-numbers #grid #recursion
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

seen = set()


def dfs(node: complex) -> float:
    """Get max path length from `node` to END."""

    if node == END:
        return 0

    s = -float("inf")  # ensure that s evaluates to zero whenever fails to reach END

    seen.add(node)  # do not return to node whilst moving down branch
    for nnode, length in GRAPH[node].items():
        if nnode not in seen:
            s = max(s, dfs(nnode) + length)
    seen.remove(node)  # free up node so that can be traversed on other branches

    return s


print(dfs(S))
