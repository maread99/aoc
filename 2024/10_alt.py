"""Day 10: Hoof It

Alternative implementat using a stack.

#DFS  #stack  #sets  #complex-numbers
"""

from aocd import get_data


raw = get_data(day=10, year=2024)

# raw = """89010123
# 78121874
# 87430965
# 96549874
# 45678903
# 32019012
# 01329801
# 10456732
# """

rows = raw.splitlines()

GRID = {}
STARTS = set()
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        lvl = int(c)
        loc = complex(i, j)
        GRID[loc] = lvl
        if not lvl:
            STARTS.add(loc)

DIRS = (-1j, 1j, -1, 1)

total_a = 0
total_b = 0
for start in STARTS:
    ends = set()
    locs = [(start, 0)]
    while locs:
        loc, lvl = locs.pop()
        for vec in DIRS:
            nloc = loc + vec
            nlvl = lvl + 1
            if GRID.get(nloc, -1) == nlvl:
                if nlvl == 9:
                    total_b += 1
                    ends.add(nloc)
                else:
                    locs.append((nloc, nlvl))
    total_a += len(ends)

print(total_a)
print(total_b)
