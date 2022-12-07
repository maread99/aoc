"""Day 7: No Space Left On Device

Revised to create tree over single iteration of data.

Uses stack to represent all directories from root to cwd.
"""
from aocd import get_data

raw = get_data(day=7, year=2022)
data = raw.splitlines()

ROOT = {}

for line in data:
    if line[0] == "$":
        if line == "$ ls":
            continue
        arg = line.split()[-1]
        if arg == "/":
            cwd = ROOT
            stack = [cwd]
        elif arg == "..":
            cwd = stack.pop()
        else:
            stack.append(cwd)
            cwd = cwd[arg]
    else:
        size, k = line.split()
        cwd.setdefault(k, {} if size == "dir" else int(size))


sizes = []
part_a = 0


def get_dir_size(dir_: dict):
    global part_a
    size = 0
    for v in dir_.values():
        size += v if isinstance(v, int) else get_dir_size(v)
    if size <= 100000:
        part_a += size
    sizes.append(size)
    return size


root_size = get_dir_size(ROOT)
print(part_a)

limit = 70000000 - 30000000
excess = root_size - limit
sizes.sort()
print(next(size for size in sizes if size > excess))
