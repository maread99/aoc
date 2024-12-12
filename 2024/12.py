"""Day 12: Garden Groups

part a: 45mins
Pleased with this time for the first part, although suspect there might have
been a much quicker way to do it. I was conscious of wanting to get things
set up as best I could for whatever part b held in store...

part b: 67mins
Identifies 'sides' with a 2-tuple key where:
    [0] the direction a bird would look to see the side from just inside
    the plot perimeter. For example, UP if the side is 'above' the cell
    immediately inside the perimeter.
    [1] the value of the row or column that lies immediately next to the
    plot (on the outer side of the perimeter) in this direction.

Initially I just counted the number of 'sides' and voila, example answer
was too low. Didn't realise the error until debugging a specific plot
revealed this appraoch will count as just 1 any 'side' (as I'd defined it)
which is not continuous, such as for plot "V" in the example between the
columns indexed 1 and 2. I thought of two ways to correct for this and went
first with the wrong one (tried to add on the number of plot locations that
adjoin the 'side', but of course this only works if the side is broken by a
single location, as in the "V" region, but not if it's broken by a strip of
more than one location). Went with the much simpler original idea of, for
each 'side' adding one each time an otherwise contiguous strip of non-plot
locations (on the outer side of the perimeter) was broken by one or more
plot locations).

EDIT: I believe another way to count the number of sides would be to 'walk'
the perimeter and simply 'add a side' each time the walk changes direction,
i.e at each corner.

total: 1hour 52mins, 6.3x bottom of the leaderboard
Respectable time for me, shame I wasted a bit on part b.

#grid  #complex-numbers  #DFS
"""

import itertools
from collections import defaultdict

from aocd import get_data

raw = get_data(day=12, year=2024)

# raw  ="""RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE
# """

GRID = {}
rows = raw.splitlines()
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        GRID[complex(i, j)] = c

GRID_REV = defaultdict(set)
for loc, typ in GRID.items():
    GRID_REV[typ].add(loc)

UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRS = (UP, DOWN, LEFT, RIGHT)

typs = set(GRID_REV)

plots_all: dict[str, list[list[set[complex]]]] = {}  # type ref to list of plots
while typs:
    typ = typs.pop()
    typ_locs = GRID_REV[typ]
    plots: list[set[complex]] = []  # list of plot
    while typ_locs:
        stk = [typ_locs.pop()]
        plot: set[complex] = set([stk[0]])  # plot as set of locations
        while stk:
            loc = stk.pop()
            for d in DIRS:
                nloc = loc + d
                if nloc in typ_locs:
                    stk.append(nloc)
                    typ_locs.remove(nloc)
                    plot.add(nloc)
        plots.append(plot)
    plots_all[typ] = plots

tot = 0
for typ, plots in plots_all.items():
    for p in plots:
        area = len(p)
        prm = 0
        for loc in p:
            for d in DIRS:
                # consider as forming 1 length of perimeter every non-plot cell that's
                # adjacent to a plot cell
                if loc + d not in p:
                    prm += 1
        tot += area * prm

print(tot)


tot = 0
for typ, plots in plots_all.items():
    for p in plots:
        area = len(p)
        # `sides` is a mapping of 'side' to corresponding cells on outer side of
        # perimeter, where 'side' is as defined in module doc notes for part b
        sides = defaultdict(list)
        for loc in p:
            for d in DIRS:
                if (nloc := loc + d) not in p:
                    side = (d, nloc.imag) if d in (UP, DOWN) else (d, nloc.real)
                    sides[side].append(nloc)
        prm = len(sides)
        # correct `prm` for those 'sides' that are broken by the plot itself, and hence
        # comprise two or more actual sides.
        for (d, row_col), locs in sides.items():
            # vals as column or row values of cells along side (on outer side of perimeter)
            vals = sorted([loc.real if d in (UP, DOWN) else loc.imag for loc in locs])
            # add one actual side every time these cells do not form contiguous regions
            prm += sum((1 for a, b in itertools.pairwise(vals) if b - a != 1))
        tot += area * prm

print(tot)
