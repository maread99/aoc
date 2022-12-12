"""Day 12: Hill Climbing Algorithm.

My solution was somewhat inefficient in that would inspect coordinates seen
more than once, looking each time to see if it had found a shorter path and
if so updating seen. Most participants who publish seem to have identified
the problem as one for a Breadth First Search (BFS). Great explanation by
hyper-neutrino, and the corresponding solution:
- https://www.youtube.com/watch?v=xhe79JubaZI
- https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day12p1.py

This alt version implements a BFS. This required changing the original
solution to store the 'unfinished paths' in a deque as opposed to a list
(i.e in a queue as opposed to a stack). With this arrangement can simply
check if a coordinate had already been seen rather than checking if it's
being visited at the end of a shorter path. Why? Because using a queue
ensures that when a coordinate is visited for the first time, this IS the
shortest route to the coordinate. If it's visit again later, then it will
have been via a route of the same length or longer. `seen` can consequently
be simplified to a set.

The change in implementation means that the original approach taken for
part b cannot be replicated. Originally it was possible to run the
iterations for each starting point within the main loop, aborting each
as soon as it hit a coord that had already been evaluated on a shorter
route. This isn't possible with the BFS implemented here for part a as the
first time any interation hits a new coord that would be assumed as the
shortest route, even though a later iteration could be on a shorter path.

Instead evaluated all the starts outside of the loop and added them all
to the initial queue. This way whenever a coord is encountered for the
first time it will be on the shortest route to this coord from a valid
starting point.

An alternative for part b is to run part a in reverse, starting from E and
looking for the shortest path to a coord with value 'a'. More efficient
although in terms of getting a solution for aoc, probably quicker as
implemented here.
"""

from collections import deque

from aocd import get_data

raw = get_data(day=12, year=2022)
data = raw.splitlines()

# create heightmap
grid = {}
for j, row in enumerate(data):
    for i, h in enumerate(row):
        if h == "S":
            S = (i, j)
            grid[i, j] = ord("a")
        elif h == "E":
            E = (i, j)
            grid[i, j] = ord("z")
        else:
            grid[i, j] = ord(h)

VECS = ((0, 1), (0, -1), (1, 0), (-1, 0))

Cell = tuple[int, int]  # coord


def get_shortest_path(starts: deque[tuple[Cell, int]]) -> float:
    unfinished = starts
    shortest = float("inf")
    seen = set()
    while unfinished:
        frm, count = unfinished.popleft()
        count += 1
        h = grid[frm]
        for vec in VECS:
            new = frm[0] + vec[0], frm[1] + vec[1]
            if new not in grid:
                continue
            if grid[new] > h + 1:
                continue
            if new in seen:
                continue
            if new == E:
                if count < shortest:
                    shortest = count
                continue
            seen.add(new)
            unfinished.append((new, count))
    return shortest


start = deque([(S, 0)])  # [0] coord, [1] steps to coord
print(get_shortest_path(start))

# part b

ORD_A = ord("a")
starts: deque[tuple[Cell, int]] = deque()
for S, h in grid.items():
    if h == ORD_A:
        starts.append((S, 0))
print(get_shortest_path(starts))
