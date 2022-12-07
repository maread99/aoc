"""Day 7: No Space Left On Device

This one took me 2.5 coffees at a rate of 1 coffee / hour.
"""
import typing

from aocd import get_data

raw = get_data(day=7, year=2022)
data = raw.splitlines()


def is_cmd(line: str) -> bool:
    return line.startswith("$ ")


# Create list with each item representing one input / output
in_outs: list[tuple[str, list[str]]] = []
for line in data:
    if is_cmd(line):
        in_outs.append((line[2:], []))
        continue
    in_outs[-1][1].append(line)

# verify looks like what's expected
for in_out in in_outs:
    assert len(in_out) == 2
    if in_out[1]:
        assert in_out[0] == "ls"

Dir = dict[str, typing.Union["Dir", int]]  # where key is file int is size
ROOT = "/"
TREE: Dir = {ROOT: {}}
cwd: list[str] = []


def get_dir(path: list[str]):
    d = TREE
    for dir_ in path:
        d = d[dir_]
    return d


def write_dir_contents(path: list[str], contents: list[str]):
    d = get_dir(path)
    for c in contents:
        size, k = c.split()
        d[k] = {} if size.startswith("d") else int(size)


def chg_cwd(cwd: list[str], cmd: str):
    _, arg = cmd.split()
    if arg == "/":
        return [ROOT]
    if arg == "..":
        return cwd[:-1]
    return cwd + [arg]


for in_, out in in_outs:
    if in_.startswith("cd"):
        cwd = chg_cwd(cwd, in_)
    else:
        write_dir_contents(cwd, out)


sizes = []
part_a = 0


def get_dir_size(dir_: dict):
    global part_a
    size = 0
    for v in dir_.values():
        if isinstance(v, int):
            size += v
        else:
            size += get_dir_size(v)
    if size <= 100000:
        part_a += size
    sizes.append(size)
    return size


root_size = get_dir_size(TREE[ROOT])
print(part_a)

limit = 70000000 - 30000000
excess = root_size - limit
sizes.sort()
print(next(size for size in sizes if size > excess))


# TEST_TREE = {
#     "/": {
#         "dir": {
#             "some_file": 3322,
#             "another_file": 4455,
#             "subdir": {
#                 "file_d": 6677,
#                 "file_e": 8899,
#             },
#         },
#         "another_dir": {
#             "file_in_other_dir": 3333,
#         }
#     }
# }
