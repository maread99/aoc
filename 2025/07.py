"""Day 7: Laboratories

part 1: 19mins

part 2: 77mins
Started with a DFS (which was never going to work for anything much bigger
than the example) before identifying it as one for cached recursion.

total: 96mins
12000
#recursion  #memoization  #iteration
"""

import functools

from aocd import get_data

raw = get_data(day=7, year=2025)

# raw = """.......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
# ...............
# .....^.^.^.....
# ...............
# ....^.^...^....
# ...............
# ...^.^...^.^...
# ...............
# ..^...^.....^..
# ...............
# .^.^.^.^.^...^.
# ...............
# """


lines = raw.splitlines()
splitters = set()
for j, line in enumerate(lines):
    for i, c in enumerate(line):
        if c == "^":
            splitters.add((j, i))
        if c == "S":
            START = (j + 1, i)

# part 1
yons = {START}
total = 0
for j, line in enumerate(lines):
    for i, c in enumerate(line):
        if (j, i) in yons:
            if (j + 1, i) in splitters:
                total += 1
                yons.add((j + 1, i + 1))
                yons.add((j + 1, i - 1))
            else:
                yons.add((j + 1, i))

print(total)

# part 2
DIM = len(lines)


@functools.cache
def f(p: tuple[int, int]) -> int:
    np = (p[0] + 1, p[1])
    while np not in splitters:
        if np[0] == DIM - 1:
            return 1
        np = (np[0] + 1, np[1])
    return f((np[0], np[1] + 1)) + f((np[0], np[1] - 1))


print(f(START))
