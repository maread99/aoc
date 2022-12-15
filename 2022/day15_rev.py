"""Day 15: Beacon Exclusion Zone.

Same approach although here for part b evaluates the interval 'as-you-go'
and aborts as soon as the limits are covered. Very significantly simplifies
the code, but shaves hardly 10s off the run time, down to about 35s.
"""

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

lines = [ints(line) for line in raw.splitlines()]
lines.sort(key=lambda x: x[0])
for Y in range(LIMIT + 1):
    x = -1
    for xs, ys, xb, yb in lines:
        d = abs(xs - xb) + abs(ys - yb)
        if (ys - d) <= Y <= (ys + d):
            dx = d - abs(ys - Y)
            if xs - dx <= x:
                x = max(x, xs + dx)
                if x >= LIMIT:
                    continue
    if x < LIMIT:
        break

X = x + 1  # x coordinate will be the one following the interval
print((X * LIMIT) + Y)
