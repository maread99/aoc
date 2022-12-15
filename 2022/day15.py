"""Day 15: Beacon Exclusion Zone.

part a 68mins, taken up with:
    Considering approach - grid the lot, numpy or otherwise, or was there a quicker way
    to extract the info for just row 2000000? Went with the latter on realising that
    could, for any row, easily evaluate all intervals along the x-axis in which no beacon
    could be present, with each interval corresponding with a sensor that has a scope
    that includes that row.

    Debugging as a result of poor comprehension:
        Thought required the number of positions where beacon could be present - spent
        time unnecessarily evaluating grid bounds.

        Didn't appreciate the need to deduct the number of beacons already in the row!

part b 80mins HOWEVER:
    Identified a feasible (if not very efficient) way of doing it - for each possible
    row, evaluate the intervals and merge them. If after merging there remained more
    than one interval then that's the row and the x coordinate will be the single
    value between the two remaining intervals. The crude way to merge intervals used
    for part a was never going to cut the mustard for up to 4 million iterations.

    Wrote a version of the `include` function which was poorly implemented and shouldn't
    have worked. However, fortuitously(?), it was so bad that I included a bug which
    resulted in it actually working 😏. Ran for 8 mins to get the solution out.

    Realised the bug when tidying up. Removed the bug and the code no longer worked.
    Took a considerable amount of time to work out what was going on and fix it (not
    included in the 80mins!). Ended up with a solution that solved in 45s. Not great,
    but got it out.
"""

import collections
import re

from aocd import get_data


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


raw = get_data(day=15, year=2022)
lines = [ints(line) for line in raw.splitlines()]

Y = 2000000
beacons_in_row = set()

not_here = []
for xs, ys, xb, yb in lines:
    if yb == Y:
        beacons_in_row |= {(xb, yb)}
    d = abs(xs - xb) + abs(ys - yb)
    if (ys - d) <= Y <= (ys + d):
        dx = d - abs((ys - Y))
        not_here.append((xs - dx, xs + dx))

# this is horrible, but works for a single Y row
x_checked = set()
for rng in not_here:
    x_checked |= set(range(min(rng), max(rng) + 1))
print(len(x_checked) - len(beacons_in_row))

# part b

Interval = list[int]
LIMIT = 4000000


def include(new_interval: collections.abc.Sequence[int], existing: list[Interval]):
    """Include a `new_interval` to `existing` intervals.

    Expands the first interval of `existing` that the `new_interval`
    overlaps. If `new_interval` doesn't overlap any `existing` interval
    then adds to `existing`.
    """
    x1_, x2_ = new_interval
    if x1_ > LIMIT:
        return existing
    x1 = 0 if x1_ < 0 else x1_
    x2 = LIMIT if x2_ > LIMIT else x2_
    for intrvl in existing:
        ex1, ex2 = intrvl
        if x2 < ex1 or x1 > ex2:
            # intervals do not overlap
            continue
        intrvl[0] = min(x1, ex1)
        intrvl[1] = max(x2, ex2)
        return existing
    existing.append([x1, x2])
    return existing


def merge(intervals: list[tuple[int, int]]) -> list[Interval]:
    """Merge `intervals`."""
    rtrn: list[Interval] = []
    for intrvl in intervals:
        include(intrvl, rtrn)
    if len(rtrn) > 1:
        for _ in range(len(rtrn)):
            rtrn = include(rtrn[0], rtrn[1:])
    return rtrn


for Y in range(0, LIMIT + 1):
    not_here = []
    for xs, ys, xb, yb in lines:
        d = abs(xs - xb) + abs(ys - yb)
        if (ys - d) <= Y <= (ys + d):
            dx = d - abs((ys - Y))
            not_here.append((xs - dx, xs + dx))
    if len(merged := merge(not_here)) > 1:
        break

X = merged[0][1] + 1 if merged[0][0] == 0 else merged[1][1] + 1
print((X * LIMIT) + Y)
