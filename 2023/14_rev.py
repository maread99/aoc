"""Day 14: Parabolic Reflector Dish

Attempt at a quicker version that could get the solution out by iteration.
Didn't happen, but this one's a a lot quicker. Gets it out in a few
seconds via identification of the pattern.

EDIT: For the exemplar solution see hyper-neutrino's:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day14p2.py
That solution, as most of those that I've seen do, recognise that the pattern
will repeat whenever the grid's in the same state as it's been in before.
From there can extrapolate forwards.

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

for i, line in enumerate(arr):
    arr[i] = tilt_line(line)

locs = np.argwhere(arr == 1)  # locate the rocks
load = sum(LENGTH - locs.transpose()[1])
print(load)

# part b

loads = [load]
num_unique_loads = [1]


SAMPLE_TILTS = 1000
for i in range(1, SAMPLE_TILTS):
    arr = np.flip(arr.transpose(), axis=1)
    for i, line in enumerate(arr):
        arr[i] = tilt_line(line)
    if not i % 2:
        locs = np.argwhere(arr == 1)
    else:
        locs = np.argwhere(np.flip(arr.transpose()) == 1)
    loads.append(sum(LENGTH - locs.transpose()[1]))
    num_unique_loads.append(len(set(loads)))


# following repeats code of initial solution, solving by identifying underlying pattern

num_possibles = num_unique_loads[-1]
length = 2
# `start` is lowest index when all possible loads were registered
start = num_unique_loads.index(num_possibles)
left = loads[start : start + length]
right = loads[start + length : start + length * 2]

while not (left == right):
    length += 1
    left = loads[start : start + length]
    right = loads[start + length : start + length * 2]

pat_len = len(left)
# make sure pattern continues to repeat rather than falling within a larger pattern
for n, (strt, stop) in enumerate(itertools.pairwise(range(start, len(loads), length))):
    assert loads[strt:stop] == left
assert n > 4

ROUNDS = 4000000000 - start - 1
idx = ROUNDS % pat_len
print(left[idx])
