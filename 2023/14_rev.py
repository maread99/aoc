"""Day 14: Parabolic Reflector Dish

Attempt at a quicker version that could get the solution out by iteration.
Didn't happen, but this one's a a lot quicker. Gets it out in a few
seconds via identification of the pattern.

Rewrote the pattern identification part to recognise that the pattern
will repeat whenever the arrays' are the same at a specific point of a
cycle as they were at that point of a previous cycle. This simpler approach
seems to be the way employed by most solutions.

For an exemplar solution see hyper-neutrino's:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day14p2.py

#numpy  #matrix  #patterns
"""

import itertools
import numpy as np

from aocd import get_data

raw = get_data(day=14, year=2023)

# raw = """O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....
# """


def tilt_line(line):
    new = np.zeros(line.size, dtype="int")
    # insert solids, or return if none
    solids = np.argwhere(line == 2).flatten()
    if not solids.size:
        num_rocks = sum(line)
        new[:num_rocks] = 1
        return new
    new[solids] = 2

    # insert any rocks into part of new line pre first solid
    num_rocks = sum(line[: solids[0]])
    new[:num_rocks] = 1

    # insert any rocks into each part between solids
    for a, b in itertools.pairwise(solids):
        # print(a
        num_rocks = sum(line[a + 1 : b])
        # print(num_mobile)
        new[a + 1 : a + 1 + num_rocks] = 1

    # insert any rocks into part after lastsolid
    last = solids[-1]
    num_rocks = sum(line[last + 1 :])
    new[last + 1 : last + 1 + num_rocks] = 1

    return new


# create grid

lines = raw.splitlines()
LENGTH = len(lines[0])
arr = np.zeros((len(lines), LENGTH), dtype="int")

for j, row in enumerate(lines):
    for i, c in enumerate(row):
        if c == ".":
            continue
        arr[i, j] = 1 if c == "O" else 2

arr = np.flip(arr, axis=0)

# part a

arr_a = arr.copy()
for i, line in enumerate(arr_a):
    arr_a[i] = tilt_line(line)

locs = np.argwhere(arr_a == 1)  # locate the rocks
load = sum(LENGTH - locs.transpose()[1])
print(load)

# part b

seen = set()
arrs = []

CYCLES = 1_000_000_000
for i in range(0, CYCLES):
    as_tups = tuple(tuple(line) for line in arr)
    if as_tups in seen:
        cycle_idx = i
        break
    seen.add(as_tups)
    arrs.append(as_tups)
    for _ in range(4):
        for i, line in enumerate(arr):
            arr[i] = tilt_line(line)
        arr = np.flip(arr.transpose(), axis=1)

first_idx = arrs.index(as_tups)
pat_len = cycle_idx - first_idx
remainder = (CYCLES - first_idx) % pat_len
final_tups = arrs[first_idx + remainder]
locs = np.argwhere(np.array(final_tups) == 1)
load = sum(LENGTH - locs.transpose()[1])
print(load)
