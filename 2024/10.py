"""Day 10: Hoof It

part a: 63mins
Poor time. Identified it as a DFS. Decided on tackling with recursion
rather than a stack simply in the interests of improvement - I struggle to
get my head around recursion and am slow to implement it, as I've proved
again here. Worth it though - I do feel I 'get it' a bit more each time.
See `10_alt.py` for an implementation using a stack.

part b: 15mins

total: 78mins, 18.4x bottom of the leaderboard.

I've written both parts here separately in the interests of clarify,
although they could be easily combined in a single function (similar to how
the solution is combined in the alternative stack implementation
`10_alt.py`).

#DFS  #recursion  #sets. Also navigating a #grid with #complex-numbers
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


# part a
def get_ends(loc, lvl, ends):
    for vec in DIRS:
        nloc = loc + vec
        nlvl = lvl + 1
        if GRID.get(nloc, -1) == nlvl:
            if nlvl == 9:
                ends.add(nloc)
            else:
                ends |= get_ends(nloc, nlvl, ends)
    return ends


print(sum(len(get_ends(start, 0, set())) for start in STARTS))


# part b
def num_routes(loc, lvl):
    num = 0
    for vec in DIRS:
        nloc = loc + vec
        nlvl = lvl + 1
        if GRID.get(nloc, -1) == nlvl:
            if nlvl == 9:
                num += 1
            else:
                num += num_routes(nloc, nlvl)
    return num


print(sum(num_routes(start, 0) for start in STARTS))
