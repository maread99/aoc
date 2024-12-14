"""Day 14: Restroom Redoubt

An alternative version that seeks out the iteration where there is the
highest number of robots immediately adjacent to other robots (it's not
concerned with deduplication as each iteration is given the same
treatment). It does take notably longer to execute (few minutes maybe)
although this would have been compensated by the quicker 'write time'.

Solution here also tides up some of the superflous code on my original
solution.

Got the idea from:
    https://github.com/anli5005/advent-of-code-2024/blob/main/14/14b.py
(This solution prints the grid whenever the number of adjoining robots is
greater than an arbitrary number, letting the solver judge if that's the
one rather than waiting for all iterations to complete.)

Also, this one relies on the number of iterations before the pattern
repeats being the width * height of the grid. I kind of think it should be
obvious to me why this is, but it's not.
"""

import math
import re
from collections import defaultdict

from aocd import get_data

raw = get_data(day=14, year=2024)
W = 101
H = 103

# raw = """p=0,4 v=3,-3
# p=6,3 v=-1,-3
# p=10,3 v=-1,2
# p=2,0 v=2,-1
# p=0,0 v=1,3
# p=3,0 v=-2,-2
# p=7,6 v=-1,-3
# p=3,0 v=-1,-2
# p=9,3 v=2,3
# p=7,3 v=-1,2
# p=2,4 v=2,-3
# p=9,5 v=-3,-3
# """
# W = 11
# H = 7


REGEX = r"(?:(?<!\d)-)?\d+"
lines = [list(map(int, re.findall(REGEX, l))) for l in raw.splitlines()]

# part a

cnt = defaultdict(int)

for px, py, vx, vy in lines:
    px = (px + (vx * 100)) % W
    py = (py + (vy * 100)) % H
    cnt[(px, py)] += 1

quads = [0, 0, 0, 0]
for loc, n in cnt.items():
    if loc[0] < W // 2 and loc[1] < H // 2:
        quads[0] += n
    elif loc[0] > W // 2 and loc[1] < H // 2:
        quads[1] += n
    elif loc[0] < W // 2 and loc[1] > H // 2:
        quads[2] += n
    elif loc[0] > W // 2 and loc[1] > H // 2:
        quads[3] += n

print(math.prod(quads))

if W == 11 or H == 7:
    exit()

# part b

psts = [(l[0], l[1]) for l in lines]
vels = [(l[-2], l[-1]) for l in lines]

i = 0
max_adj = (0, 0)
for i in range((H * W)):
    npsts = []
    for (px, py), (vx, vy) in zip(psts, vels):
        px = (px + vx) % W
        py = (py + vy) % H
        npsts.append((px, py))
    psts = npsts
    i += 1

    adj = 0
    for x, y in psts:
        for vx, vy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + vx, y + vy) in psts:
                adj += 1
    if adj > max_adj[0]:
        max_adj = (adj, i)

it = max_adj[1]

grid = [["."] * W for _ in range(H)]
for px, py, vx, vy in lines:
    px = (px + (vx * it)) % W
    py = (py + (vy * it)) % H
    grid[py][px] = "X"

print("\n".join(["".join(r) for r in grid]))
print(it)
