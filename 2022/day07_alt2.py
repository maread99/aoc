"""Day 7: No Space Left On Device

Very heavily inspired by this tremendous solution...
    https://github.com/MasterMedo/aoc/blob/394b4b2e6c20e7485a008c50c39fd4bbacb2526e/2022/day/7.py
...which makes excellent use of the `itertools.accumulate` function to create all paths
along the cwd. Also employs Strutural Pattern Matching.
"""

from collections import defaultdict
from itertools import accumulate

from aocd import get_data

raw = get_data(day=7, year=2022)
data = raw.splitlines()

cwd = []
dirs = defaultdict(int)  # key path, value size

for line in data:
    match line.split():
        case _, _, "..":
            cwd.pop()
        case _, "cd", dir_:
            cwd.append(dir_)
        case "$" | "dir", *_:
            continue
        case size, _:
            for path in accumulate(cwd, lambda a, n: a + "/" + n):
                dirs[path] += int(size)

print(sum((size for size in dirs.values() if size <= 100000)))

limit = 70000000 - 30000000
excess = dirs["/"] - limit
print(next(size for size in sorted(list(dirs.values())) if size > excess))
