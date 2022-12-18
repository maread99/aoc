"""Day 18: Boiling Boulders.

part a: 65mins (50mins before and 10mins after representing the example
on 6 postits, one for each level).

part b: few hours, discontinuous.
Started badly by considering fully enclosed cubes rather than hollows. Then
started evaluating hollows before realising how simple it would be to
map the exterior. (Was prejudiced by the example's reference to hollows.
Should have instead taken a step back at the start and considered the
problem more globally.)

Only issue after identifying the approach was defining the search space as
a cube and failing to provide a margin around the edge to inspect the
sides that were butted up against the edges of the search space boundaries.

On reflection, although not an issue here given the number of cubes, would
have been more efficient to have not wasted time inspecting empty space and
instead started on a cube with a exterion surface and wandered around the
lava surface from there.
"""

from collections import defaultdict, deque
import re

from aocd import get_data

raw = get_data(day=18, year=2022)


def ints(s: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


CUBES = frozenset(map(ints, raw.splitlines()))

grid = defaultdict(set)
for x, y, z in CUBES:
    grid[z].add((x, y))

SIDES = len(CUBES) * 6
t = 0  # evaluate number of sides shared by two cubes...
for z in range(min(grid), max(grid) + 1):
    for x, y in grid[z]:  # on each level
        for x_, y_ in grid[z]:
            if x == x_ and y == y_:
                continue
            if (x == x_ and y == y_ + 1) or ((y == y_ and x == x_ + 1)):
                t += 1  # add one if neighbours with a cube on same level
        if z + 1 in grid:
            for x1, y1 in grid[z + 1]:
                if x == x1 and y == y1:
                    t += 1  # add one if neighbours with cube on level 'below'

# all sides that aren't shared by neighbours are surface
print(SIDES - (t * 2))

# part b

xs, ys, zs = zip(*CUBES)
MIN_X, MAX_X = min(xs), max(xs)
MIN_Y, MAX_Y = min(ys), max(ys)
MIN_Z, MAX_Z = min(zs), max(zs)

# evaluate a point in space outside the lava
for i in range(MAX_X + 1):
    if (start := (i, MIN_Y, MIN_Z)) not in CUBES:
        break


def get_adjs(cube) -> set:
    x, y, z = cube
    adjs = set()
    if x - 1 >= MIN_X - 1:
        adjs.add((x - 1, y, z))
    if x + 1 <= MAX_X + 1:
        adjs.add((x + 1, y, z))
    if y - 1 >= MIN_Y - 1:
        adjs.add((x, y - 1, z))
    if y + 1 <= MAX_Y + 1:
        adjs.add((x, y + 1, z))
    if z - 1 >= MIN_Z - 1:
        adjs.add((x, y, z - 1))
    if z + 1 <= MAX_Z + 1:
        adjs.add((x, y, z + 1))
    return adjs


# walk around the exterior, counting sides
seen = set((start,))
q = deque((start,))
surfs = []
t = 0
walked = set()
while q:
    cube = q.popleft()
    adjs = get_adjs(cube)
    space = adjs - CUBES
    if surfaces := adjs - space:
        surfs.extend(list(surfaces))
        walked.add((cube, tuple(surfaces)))
        t += len(surfaces)  # these are exterior surfaces
    q.extend(space - seen)
    seen |= space

print(t)
