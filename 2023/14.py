"""Day 14: Parabolic Reflector Dish

part a: 34mins
Silly bugs.

part b: 2hrs 45mins
Clear that the part a implementation was not going to reach anywhere near
a billion cycles. Two routes to a solution occurred to me. Either, a much
faster implementation that could iterate all the way to a billion cycles,
or any implementation that could iterate through enough cycles to establish
a pattern in the loads.

Questioned if the pattern wouldn't be too long to establish itself within a
reasonable time (relative to the time of execution for a single tilt).
Adapted the part a solution for 4 tilt directions and with the example data
established that there was a pattern that came out pretty quickly. Also came
out 'quick enough' for the real data (1000 cycles in under 2 mins). Then
just extrapolated the pattern forward to coincide with the required cycle.

Had to resolve numerous bugs:
    Hadn't accommodated different bounds for directions other than north.

    At the start of a new tilt I hadn't changed the order that the rocks
    should be moved in to correspond with the direction (i.e. should be
    'lowest' rock first, with 'lowest' considered in the physical sense).

    Had misinterpreted 'cycle', thinking that required 1 billion tilts
    rather than 4 billion tilts. (I actually solved before realising this
    bug by way of earlier attempts being 'too high' and 'too low'. Knowing
    the possible loads (i.e. the 36 in the pattern) I was able to get the
    answer out in 5 attempts, although couldn't understand why the pattern
    wasn't aligning until I reread the part b text more carefully and
    realised I'd confused a cycle with a tilt.)

Other comments:
    The load doesn't change (from the prior load) when the tilt is east or
    west, although if this information is useful then it's not obvious to
    me why.

total: 199mins, 11.5x bottom of the leaderboard.

Thoughts on how to implement a faster implementation:
    Work row by row or column by column, there's no need to be looking at
    the whole grid when moving a rock.

    And no need to move a rock one cell at a time, rather by inspection of
    a row or column can easily advance each rock in turn to its new
    position.

    Should just need a single bit of code to move rocks along a line (be
    that line a 'row' or a 'column'). SHOULD HAVE REALISED THIS AT THE
    START of part b which would probably have led to working line by line
    first time around.

    Even then, given the need to complete 4 billion tilts, wonder if might
    not still have to resort to pattern identification and extrapolating
    forwards...?

#complex-numbers  #sets  #sort  #grid  #patterns
"""

import itertools
import math

from aocd import get_data

raw = get_data(day=14, year=2023)

raw = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

# create grid

STUCK = set()
MOBILE = []

rows = raw.splitlines()
NUM_ROWS = len(rows)
NUM_COLS = len(rows[0])

for j, row in enumerate(rows):
    for i, c in enumerate(row):
        if c == "O":
            MOBILE.append(complex(i, j))
        if c == "#":
            STUCK.add(complex(i, j))

NORTH = complex(0, -1)  # up negative

# part a

# popping off list, want to move furthest north first
mobile = list(reversed(MOBILE.copy()))
final = set()

for i in range(len(mobile)):
    rock = mobile.pop()
    while True:
        if rock.imag == 0:
            final.add(rock)
            break
        nrock = rock + NORTH
        if nrock in STUCK or nrock in mobile or nrock in final:
            final.add(rock)
            break
        rock = nrock

total = 0
for rock in final:
    level = abs(int(rock.imag) - NUM_ROWS)
    total += level

print(total)

# part b

# down positive, up negative
# right postiive, left negative
WEST = complex(-1, 0)
SOUTH = complex(0, 1)
EAST = complex(1, 0)
direction = itertools.cycle((NORTH, WEST, SOUTH, EAST))

Y_LIMITS = {
    NORTH: 0,
    EAST: math.inf,
    WEST: math.inf,
    SOUTH: NUM_ROWS - 1,
}

X_LIMITS = {
    NORTH: math.inf,
    EAST: NUM_COLS - 1,
    WEST: 0,
    SOUTH: math.inf,
}

# CYCLES = 1_000_000_000
SAMPLE_SIZE = 1000

mobile = final = MOBILE.copy()
loads = []
num_unique_loads = []
for _ in range(SAMPLE_SIZE):
    next_dir = next(direction)
    x_limit, y_limit = X_LIMITS[next_dir], Y_LIMITS[next_dir]
    mobile = list(final)
    final = set()

    if next_dir == NORTH:
        mobile.sort(key=lambda x: x.imag, reverse=True)
    elif next_dir == SOUTH:
        mobile.sort(key=lambda x: x.imag)
    elif next_dir == EAST:
        mobile.sort(key=lambda x: x.real)
    else:
        mobile.sort(key=lambda x: x.real, reverse=True)

    for _ in range(len(mobile)):
        rock = mobile.pop()
        while True:
            if rock.imag == y_limit or rock.real == x_limit:
                final.add(rock)
                break
            nrock = rock + next_dir
            if nrock in STUCK or nrock in mobile or nrock in final:
                final.add(rock)
                break
            rock = nrock

    load = 0
    for rock in final:
        level = abs(int(rock.imag) - NUM_ROWS)
        load += level
    loads.append(load)
    num_unique_loads.append(len(set(loads)))


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
