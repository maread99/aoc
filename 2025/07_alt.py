"""Day 7: Laboratories

The DFS solution that I was originally trying to get out.

#DFS  #memoization
"""

from collections import defaultdict

from aocd import get_data


# raw = get_data(day=7, year=2025)

raw = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

# combined solution

lines = raw.splitlines()
splitters = set()

for j, line in enumerate(lines):
    for i, c in enumerate(line):
        if c == "S":
            FIRST = (j + 2, i)
        if c == "^":
            splitters.add((j, i))

# state as [(path_start), splitter]
stack = [((FIRST[0], FIRST[1] + 1), FIRST), ((FIRST[0], FIRST[1] - 1), FIRST)]
LIMIT = len(lines) - 1
# cache number of paths from a splitter
cache: dict[tuple[int, int], int] = defaultdict(int)

while stack:
    p, splitter = stack.pop()
    np = (p[0] + 1, p[1])
    while np not in splitters:
        if np[0] == LIMIT:
            cache[splitter] += 1
            break
        np = (np[0] + 1, np[1])
    if np[0] == LIMIT:
        continue

    assert np in splitters
    if np in cache:
        cache[splitter] += cache[np]
        continue
    stack.append((p, splitter))  # put back on stack as not resolved
    stack.append(((np[0], np[1] + 1), np))
    stack.append(((np[0], np[1] - 1), np))

print(len(cache))  # part 1
print(cache[FIRST])  # part 2
