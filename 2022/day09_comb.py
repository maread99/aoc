"""Day 9: Rope Bridge

Also adds seen positions to a set rather than looking in a list and
appending if not otherwise there - cleaner.
"""

from aocd import get_data
import numpy as np

raw = get_data(day=9, year=2022)

data = raw.splitlines()

VECS = {
    "U": np.array((0, 1)),
    "D": np.array((0, -1)),
    "L": np.array((-1, 0)),
    "R": np.array((1, 0)),
}

knots = [np.array((0, 0)) for _ in range(10)]
part_a = {(knots[1][0], knots[1][1])}
part_b = {(knots[-1][0], knots[-1][1])}
for line in data:
    direction, num = line.split()
    vec = VECS[direction]
    for _ in range(int(num)):
        knots[0] += vec
        for i, t in enumerate(knots[1:]):
            h = knots[i]
            if (np.abs(h - t) > 1).any():
                # move knot towards knot that it follows
                d = h - t
                bv = np.abs(d) > 1
                d[bv] = d[bv] / np.abs(d[bv])  # chg any 2 to 1, retaining sign
                t += d
                if i == 0:
                    part_a.add((t[0], t[1]))
                if i == len(knots) - 2:
                    part_b.add((t[0], t[1]))

print(len(part_a))
print(len(part_b))
