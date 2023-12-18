"""Day 17: Clumsy Crucible

Uses Dijkstra's algorithm to employ a priority queue (heap) such that the
lowest cost part is always at the front of the queue, and consequently when
you first find the end, you've go there along the lowest cost route.

Simpler than the original implementation as the priority queue is the
optimization, no need to create a cache of for every circumstance that's
been seen before, just save the states to a set.

Vectors changed to tuples (rather than complex numbers) to accommodate use
of heap. Also took change as opportunity to have first value represent rows
and second columns. 

#Dijkstra
"""

import heapq

from aocd import get_data

raw = get_data(day=17, year=2023)

# raw = """2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533
# """

# Direction Vectors
# up negative, down positive
# left negative, up position
# (row, column)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

rows = raw.splitlines()

GRID = {}
# create grid
for j, row in enumerate(rows):
    for i, c in enumerate(row):
        GRID[(j, i)] = int(c)

assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

END = (DIM - 1, DIM - 1)

# part a

# compared to original implemenation changes order of tuple to have accumulated
# heat loss as the first item which the queue will be sorted by
# tuples of accumulated heatloss, loc, (prior direcion, count of prior direction)
queue = [
    (GRID[(0, 1)], (0, 1), (RIGHT, 1)),
    (GRID[(1, 0)], (1, 0), (DOWN, 1)),
]
heapq.heapify(queue)  # make sure ordered

seen = set()

while queue:
    heat, loc, (pd, pd_count) = heapq.heappop(queue)

    if loc == END:
        ans = heat
        break

    for d in DIRECTIONS:
        if complex(*d) == -complex(*pd):
            continue

        if d == pd:
            if pd_count == 3:
                continue
            else:
                npd_count = pd_count + 1
        else:
            npd_count = 1

        nloc = (loc[0] + d[0], loc[1] + d[1])
        if nloc[0] < 0 or nloc[0] >= DIM or nloc[1] < 0 or nloc[1] >= DIM:
            continue  # out of bounds

        nheat = heat + GRID[nloc]

        key = (nloc, d, npd_count)
        if key in seen:
            continue

        seen.add(key)
        heapq.heappush(queue, (nheat, nloc, (d, npd_count)))

print(ans)

# part b

queue = [
    (sum(GRID[(0, i)] for i in range(1, 5)), (0, 4), (RIGHT, 4)),
    (sum(GRID[(i, 0)] for i in range(1, 5)), (4, 0), (DOWN, 4)),
]
heapq.heapify(queue)  # make sure ordered

seen = set()

while queue:
    heat, loc, (pd, pd_count) = heapq.heappop(queue)

    if loc == END:
        ans = heat
        break

    for d in DIRECTIONS:
        if complex(*d) == -complex(*pd):
            continue
        if d == pd:
            if pd_count == 10:
                continue
            else:
                npd_count = pd_count + 1
        else:
            npd_count = 4

        factor = 1 if d == pd else 4
        nloc = loc[0] + (d[0] * factor), loc[1] + (d[1] * factor)
        if nloc[0] < 0 or nloc[0] >= DIM or nloc[1] < 0 or nloc[1] >= DIM:
            continue  # out of bounds

        if d == pd:
            nheat = heat + GRID[nloc]
        else:
            nheat = heat + sum(GRID[(loc[0] + (d[0] * i), loc[1] + (d[1] * i))] for i in range(1, 5))

        key = nloc, (d, npd_count)
        if key in seen:
            continue
        seen.add(key)


        heapq.heappush(queue, (nheat, nloc, (d, npd_count)))

print(ans)
