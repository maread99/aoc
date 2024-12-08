"""Day 8: Resonant Collinearity

part a: 17mins
part b: 12mins
I didn't at first appreciate that antenna locations were antinodes. I
did a manual glance at the antenna data and saw that there was more than
one antenna for every frequency (which I ASSUME is the case for everyone's
data), hence ALL antenna locations are also antinodes.

total: 29mins, 4.0x bottom of the leaderboard.

#sets  #complex-numbers  #vectors  #combinations
"""

import itertools
from collections import defaultdict

from aocd import get_data


raw = get_data(day=8, year=2024)

# raw = """............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............
# """

rows = raw.splitlines()

ant = defaultdict(list)
ANTS = set()
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        if c != ".":
            ant[c].append(complex(i, j))
            ANTS.add(complex(i, j))


assert len(rows) == len(rows[0])
LIMIT = len(rows) - 1

locs = set()
for vals in ant.values():
    for a, b in itertools.combinations(vals, 2):
        vec = b - a
        for loc in (b + vec, a - vec):
            if 0 <= loc.real <= LIMIT and 0 <= loc.imag <= LIMIT:
                locs.add(loc)
print(len(locs))

locs = set()
for vals in ant.values():
    for a, b in itertools.combinations(vals, 2):
        vec = b - a
        loc = b + vec
        while 0 <= loc.real <= LIMIT and 0 <= loc.imag <= LIMIT:
            locs.add(loc)
            loc += vec
        loc = a - vec
        while 0 <= loc.real <= LIMIT and 0 <= loc.imag <= LIMIT:
            locs.add(loc)
            loc -= vec
print(len(ANTS | locs))
