"""Day 9: Movie Theater

part 1: 14mins

part 2: >8hours...
This one sapped my Christmas spirit.

This implementation describes the exterior around the boundary and then
rejects any rectangle with any edge that enters this exterior.

Took an age because I just couldn't get the answer out with an earlier
more complex implementation which I gave up. Then went with this different
approach although it oringally gave me the exact same wrong answer as I was
getting with the earlier implemenation! Went over the part that the two
implementations had in common and realised that, of all things, there was a
bug in how I was calculating the area!! The bug didn't effect the answer
for the example or part 1 so I didn't think to look there! Should have
done. With the area bug corrected the original implementation works too
(09_alt.py).

What a disaster.

total: >8hours
23500
#bisect
"""

import itertools
from bisect import bisect
from collections import defaultdict

from aocd import get_data

raw = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

# raw = get_data(day=9, year=2025)

tiles = [tuple(map(int, line.split(","))) for line in raw.splitlines()]

# part 1
max_ = 0
for i_, (x, y) in enumerate(tiles[:-1]):
    for x2, y2 in tiles[i_ + 1 :]:
        area = (abs(x2 - x) + 1) * (abs(y - y2 + 1))
        max_ = max_ if max_ > area else area

print(max_)

# part 2

top_left = min(tiles)
nxt = tiles[tiles.index(top_left) + 1]
if top_left[1] != nxt[1]:
    # path around boundary described in anticlockwise direction, make it clockwise
    tiles.reverse()

# evaluate cells on the boundary that are immediately adjacent to tiles.
in_boundary = set()
for (x, y), (x2, y2) in zip(tiles, itertools.cycle(tiles[1:]), strict=False):
    if y == y2:
        in_boundary.add((min(x, x2) + 1, y))
        in_boundary.add((max(x, x2) - 1, y))
    else:
        in_boundary.add((x, min(y, y2) + 1))
        in_boundary.add((x, max(y, y2) - 1))

# describe the exterior immediately adjacent to the boundary. Don't worry
# about corners - they wouldn't serve any purpose anyway.
EXTERIOR_I: dict[int, list[int]] = defaultdict(list)
EXTERIOR_J: dict[int, list[int]] = defaultdict(list)
for (x1, y1), (x2, y2) in zip(tiles, itertools.cycle(tiles[1:]), strict=False):
    if y1 == y2:
        y = y1 - 1 if x2 > x1 else y1 + 1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            # ignore the inticacies of inner and outer corners by considering
            # all cells adjacent to a boundary section (i.e. a run between tiles)
            # and then ignoring ones at the extremes if they coincide with the
            # boundary (whether either does coincide or not will depend on the
            # direction of the previous and next run).
            if (x, y) in in_boundary:
                continue
            EXTERIOR_I[x].append(y)
    else:
        x = x1 + 1 if y2 > y1 else x1 - 1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if (x, y) in in_boundary:
                continue
            EXTERIOR_J[y].append(x)

for v in EXTERIOR_I.values():
    v.sort()
for v in EXTERIOR_J.values():
    v.sort()

max_ = 0
for n, (x, y) in enumerate(tiles[:-1]):
    for x2, y2 in tiles[n + 1 :]:
        area = (abs(x2 - x) + 1) * (abs(y - y2) + 1)
        if area <= max_:
            continue

        # ignore any rectangle with an edge that crosses the padding.
        if bisect(EXTERIOR_J[y], x) != bisect(EXTERIOR_J[y], x2):
            continue
        if bisect(EXTERIOR_J[y2], x) != bisect(EXTERIOR_J[y2], x2):
            continue
        if bisect(EXTERIOR_I[x], y) != bisect(EXTERIOR_I[x], y2):
            continue
        if bisect(EXTERIOR_I[x2], y) != bisect(EXTERIOR_I[x2], y2):
            continue

        max_ = max(max_, area)

print(max_)
