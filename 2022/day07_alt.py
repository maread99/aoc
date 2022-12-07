"""Day 7: No Space Left On Device

All-in-one solution, evaluate sizes on single walk through of the data,
avoiding recursion.

Written after seeing solution:
    https://github.com/James-Ansley/adventofcode/blob/2e0e6f005fd72a9f5b7c572809a31a8f05d6bc45/2022/day07.py
"""
from aocd import get_data

raw = get_data(day=7, year=2022)
data = raw.splitlines()

sizes = []
stack: list[int] = []  # sizes in each dir to cwd

for line in data:
    if line == "$ ls" or line.startswith("dir"):
        continue

    if line[0] == "$":
        arg = line.split()[-1]
        if arg == "..":
            child_size = stack.pop()
            stack[-1] += child_size
            sizes.append(child_size)
        else:
            stack.append(0)
    else:
        size, _ = line.split()
        stack[-1] += int(size)

while stack:  # clear any remaining stack
    child_size = stack.pop()
    if stack:
        stack[-1] += child_size
    sizes.append(child_size)

print(sum((size for size in sizes if size <= 100000)))

limit = 70000000 - 30000000
excess = sizes[-1] - limit
print(next(size for size in sorted(sizes) if size > excess))
