"""Day 9: Rope Bridge

a 1hr, b 12mins.
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
h, t = np.array((0, 0)), np.array((0, 0))

seen = [(t[0], t[1])]
for line in data:
    direction, num = line.split()
    vec = VECS[direction]
    for _ in range(int(num)):
        h += vec
        if (np.abs(h - t) > 1).any():
            # move tail towards h
            d = h - t
            bv = np.abs(d) > 1
            d[bv] = d[bv] / np.abs(d[bv])  # chg any 2 to 1, retaining sign
            t += d
            if (t_ := (t[0], t[1])) not in seen:
                seen.append(t_)
print(len(seen))


# part b

knots = [np.array((0, 0)) for _ in range(10)]
seen = [(knots[-1][0], knots[-1][1])]
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
                d[bv] = d[bv] / np.abs(d[bv])
                t += d
                if i == (len(knots) - 2) and (t_ := (t[0], t[1])) not in seen:
                    seen.append(t_)

print(len(seen))
