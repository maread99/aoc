"""Day 14: Restroom Redoubt

hyperneutrino shows the actual way to do this:
    https://github.com/hyperneutrino/advent-of-code/blob/main/2024/day14p2.py

hyperneutrino was the only person I saw who realised / guessed the link
with part a -> As the tree is centered in the middle of the grid, the
effect of not including robots lying on these center lines is to
minimise the safety factor on the iteration with the tree. Neat. It does
require assuming that the tree is centered on the grid, but certainly worth
a go given the minimal 'write time' and that part a was probably showing
the way forward!

My version here also tides up some of the superflous code on my original
solution.

#vectors
"""

import math
import re
from collections import Counter, defaultdict

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


def evaluate_safety(cnt: Counter):
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
    return math.prod(quads)


# part a

cnt = defaultdict(int)

for px, py, vx, vy in lines:
    px = (px + (vx * 100)) % W
    py = (py + (vy * 100)) % H
    cnt[(px, py)] += 1

print(evaluate_safety(cnt))

if W == 11 or H == 7:
    exit()

# part b

min_safety = (math.inf, -1)
for i in range(W * H):
    cnt = defaultdict(int)
    for px, py, vx, vy in lines:
        px = (px + (vx * i)) % W
        py = (py + (vy * i)) % H
        cnt[(px, py)] += 1
    if (safety := evaluate_safety(cnt)) < min_safety[0]:
        min_safety = (safety, i)

it = min_safety[1]

grid = [["."] * W for _ in range(H)]
for px, py, vx, vy in lines:
    px = (px + (vx * it)) % W
    py = (py + (vy * it)) % H
    grid[py][px] = "X"

print("\n".join(["".join(r) for r in grid]))
print(it)
