"""Day 8: Playground

part 1: 94mins
Initially failed to account for the possiblity that both junction boxes
were already connected to different circuits. Only realised the error by
debugging the example line by line.

Overcomplicated it initially by thinking (perhaps not unreasonably) that if
two junction boxes were already in the same circuit then this wouldn't
count towards the number of connections made (i.e. towards the 10 in the
first example).

part 2: 7mins

total: 101mins
10862
#structural-pattern-matching #sets
"""

import math

from aocd import get_data

# raw = get_data(day=8, year=2025)

raw = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

# part 1 and 2 combined

lines_ = raw.splitlines()
lines = [tuple(map(int, line.split(","))) for line in lines_]

# tuple[distance, 2-tuple[line number of each of the two junction boxes]]
dists: list[tuple[float, tuple[int, int]]] = []
for i, (x, y, z) in enumerate(lines):
    for i2, (x2, y2, z2) in enumerate(lines[i+1:]):
        dists.append((((x-x2)**2 + (y-y2)**2 + (z-z2)**2)**(1/2), (i, i2+i+1)))

dists.sort()  # order by distance

INSPECT_AT = 10 if len(lines) == 20 else 1000
circuits: list[set] = []

for i_, (_, (i, i2)) in enumerate(dists):
    if i_ == INSPECT_AT:
        lens = sorted([len(c) for c in circuits])
        print(math.prod(lens[-3:]))
    one: set | None = None
    two: set | None = None
    for c in circuits:  # find which, if any, circuits that boxes are already in
        if one is not None and two is not None:
            break
        if one is None and i in c:
            one = c
        if two is None and i2 in c:
            two = c
    match (one, two):
        case (None, None):
            circuits.append({i, i2})
        case (None, two):
            two |= {i, i2}
        case (one, None):
            one |= {i, i2}
        case (one, two) if one is not two:
            circuits = [c for c in circuits if c not in [one, two]]
            circuits.insert(0, one | two)
        case _:
            assert one is two  # no action, already in same circuit
    if len(circuits) == 1 and len(circuits[0]) == len(lines):
        break

print(lines[i][0] * lines[i2][0])
