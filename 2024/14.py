"""Day 14: Restroom Redoubt

part a: 27mins

part b: 3hours 23mins
"Find the Easter Egg". Whaaaaaat??!! ...A different type of puzzle.

I wondered if it had something to do with part a and looked to see if all
the robots ever ended in just one quadrant. Nope.

Played around on paper with what the tree could look like, until I re-read
the question and saw that "most of the robots should arrange themselves".
That only 'MOST'. So what arrangement of robots are we actually looking
for!?

I realised with some relief that the pattern repeated relatively quickly,
within 10500 iterations (77 for the example). Printed off a represention of
the robots for all the example iterations and couldn't see a tree. Accepted
that the example wasn't going to offer any hints and printed the
representations for the actual input to files, at 100 a time. After looking
through a few of them I decided to read back those files and look for a
string "XXXXXXXXXX" in them (where "X" is a robot) and voila, it popped
out. That's how I actually solved it. The solution here looks for the same
alignment of 10 robots, albeit without the speed penalty of evaluating a
string (representing the robots) on every iterations.

This solution also prints the representation of the robots on the iteration
that the Easter Egg appears.

total: 3hours 50mins, 14.6x bottom of the leaderboard.

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

# part a

cnt = defaultdict(int)

for px, py, vx, vy in lines:
    for _ in range(100):
        px += vx
        if px < 0 or px >= W:
            px = px % W
        py += vy
        if py < 0 or py >= H:
            py = py % H
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
break_ = False
while True:
    npsts = []
    for (px, py), (vx, vy) in zip(psts, vels):
        px += vx
        if px < 0 or px >= W:
            px = px % W
        py += vy
        if py < 0 or py >= H:
            py = py % H
        npsts.append((px, py))
    psts = npsts
    i += 1

    xs, ys = zip(*psts)
    cnt_ys = Counter(ys)
    # only consider rows in which there are more than 20 robots
    rows = [r for r, num in cnt_ys.items() if num >= 20]
    if not rows:
        continue
    for r in rows:
        # look for a row with a strip of 10 contiguous robots
        col_idxs = sorted([p[0] for p in psts if p[1] == r])
        pidx = col_idxs[0]
        adj = 0
        for idx in col_idxs[1:]:
            if idx == pidx:  # more than one robot on same location
                pass
            elif idx == pidx + 1:
                adj += 1
                if adj >= 10:
                    break_ = True
                    break
            else:
                adj = 0
            pidx = idx
        if break_:
            break
    if break_:
        break

s = ""
for j in range(H):
    for i_ in range(W):
        c = "X" if (i_, j) in psts else "."
        s += c
    s += "\n"

print(s, i, sep="\n")
