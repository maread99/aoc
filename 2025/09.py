"""Day 9: Movie Theater

part 1: 14mins

part 2: >8hours...
This one sapped my Christmas spirit.

This implementation finds the boundary and then describes another path
which sits one cell towards the exterior of the boundary. Rectangles with
any edge that enters this exterior path are rejected.

Took an age because I just couldn't get the answer out with an earlier
more complex implementation which I gave up. Then went with this different
approach although it oringally gave me the exact same wrong answer as I was
getting with the earlier implemenation! Went over the part that the two
implementations had in common and realised that, of all things, there was a
bug in how I was calculating the area!! The bug didn't effect the answer
for the example or part 1 so I didn't think to look there! Should have
done. With the area bug corrected the original implementation works too
(09_alt.py) and executes pretty much instantly (this one takes 5 seconds
on my machine).

What a disaster.

total: >8hours
23500
#bisect
"""

from bisect import bisect
from collections import defaultdict

from aocd import get_data

# raw = get_data(day=9, year=2025)

raw = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

lines = [tuple(map(int, line.split(","))) for line in raw.splitlines()]

# part 1
max_ = 0
for i_, (i, j) in enumerate(lines[:-1]):
    for i2, j2 in lines[i_+1:]:
        area = (abs(i2 - i) + 1) * (abs(j - j2 + 1))
        max_ = max_ if max_ > area else area

print(max_)

# part 2

# Walk and record the boundary path from from the 'top left' corner
TL_CORNER = sorted(lines)[0]
idx = lines.index(TL_CORNER)
lines = lines[idx:] + lines[:idx]

PATH = []
ip, jp = lines[-1][0], lines[-1][1]
for i, j in lines:
    if i == ip:
        step = 1 if j > jp else -1
        for j_ in range(jp, j + step, step):
            np = (i, j_)
            if not PATH or PATH[-1] != np:
                PATH.append(np)
    else:
        assert j == jp
        step = 1 if i > ip else -1
        for i_ in range(ip, i + step, step):
            np = (i_, j)
            if not  PATH or PATH[-1] != np:
                PATH.append(np)
    ip, jp = i, j

assert PATH[0] == PATH[-1]
_ = PATH.pop()
BOUNDARY = set(PATH)

# identify if walked the boundary in an anticlockwise or clockwise direction
i, j = lines[0][0], lines[0][1]
ni, nj = lines[1][0], lines[1][1]
DIR = "AC" if i == ni else "C"

# define a path that pads the boundary out one cell towards the exterior.
# don't worry about corners - they wouldn't serve any purpose anyway.
PAD_PATH = []
for n, (i, j) in enumerate(lines):
    ni, nj = (lines[0][0], lines[0][1]) if n == len(lines) - 1 else (lines[n+1][0], lines[n+1][1])

    if j == nj:
        if ni > i:  # going right
            for i_ in range(i, ni + 1):
                PAD_PATH.append((i_, j-1 if DIR == "C" else j+1))
        else:  # going left
            for i_ in range(ni, i + 1):
                PAD_PATH.append((i_, j+1 if DIR == "C" else j-1))
    else:
        assert i == ni, (f"{n=}, {(i, j)=}, {(ni, nj)=}")
        if nj > j:  # going down
            for j_ in range(j, nj + 1):
                PAD_PATH.append((i+1 if DIR == "C" else i-1, j_))
        else:  # going up
            for j_ in range(nj, j + 1):
                PAD_PATH.append((i-1 if DIR == "C" else i+1, j_))


# the way PAD_PATH was defined it overlaps the boundary at some points
PADDING = set(PAD_PATH) - BOUNDARY

# Describe the padding by row and by column
PADDING_I: dict[int, list[int]] = defaultdict(list)
PADDING_J: dict[int, list[int]] = defaultdict(list)

for (i, j) in PADDING:
    PADDING_I[i].append(j)
    PADDING_J[j].append(i)

for v in PADDING_I.values():
    v.sort()
for v in PADDING_J.values():
    v.sort()


max_ = 0
for n, (i, j) in enumerate(lines[:-1]):
    for i2, j2 in lines[n+1:]:
        area = (abs(i2 - i) + 1) * (abs(j - j2) + 1)
        if area <= max_:
            continue

        # ignore any rectangle with an edge that crosses the padding.
        if bisect(PADDING_J[j], i) != bisect(PADDING_J[j], i2):
            continue
        if bisect(PADDING_J[j2], i) != bisect(PADDING_J[j2], i2):
            continue
        if bisect(PADDING_I[i], j) != bisect(PADDING_I[i], j2):
            continue
        if bisect(PADDING_I[i2], j) != bisect(PADDING_I[i2], j2):
            continue

        max_ = max_ if max_ > area else area

print(max_)
