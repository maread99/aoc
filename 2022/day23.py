"""Day 23: Unstable Diffusion.

part a, 67mins.

part b, 40mins of which 16mins execution and a further 11mins an aborted
execution.

Subsequently reduced execution to 12mins (version here) by reducing the
list manipulations (although for the real deal see the revised version).
"""

from collections import deque
from datetime import datetime

from aocd import get_data

start_time = datetime.now()

raw = get_data(day=23, year=2022)
lines = raw.splitlines()

dirs = deque(
    [
        (-1j, (-1 - 1j, -1j, 1 - 1j)),
        (1j, (-1 + 1j, 1j, 1 + 1j)),
        (-1, (-1 - 1j, -1, -1 + 1j)),
        (1, (1 - 1j, 1, 1 + 1j)),
    ]
)

ALL_DIRS = []
for _, ds in dirs:
    ALL_DIRS.extend(list(ds))

elves = []
for j, line in enumerate(lines):
    for i, char in enumerate(line):
        if char == "#":
            elves.append(complex(i, j))

for _ in range(10):
    no_go = set()
    prop_elves = {}
    for i, elf in enumerate(elves):
        if not any(elf + d in elves for d in ALL_DIRS):
            continue

        for d, view_dirs in dirs:
            if not any(elf + view_dir in elves for view_dir in view_dirs):
                nelf = elf + d
                if nelf in prop_elves:
                    no_go.add(nelf)
                else:
                    prop_elves[nelf] = i
                break

    for prop_elf in set(prop_elves) - no_go:
        i = prop_elves[prop_elf]
        elves[i] = prop_elf

    dirs.rotate(-1)

cs = max(elf.real for elf in elves) - min(elf.real for elf in elves) + 1
rs = max(elf.imag for elf in elves) - min(elf.imag for elf in elves) + 1
print(int((cs * rs) - len(elves)))

# part b, same approach as part a, breaking now when no elves to move

dirs = deque(
    [
        (-1j, (-1 - 1j, -1j, 1 - 1j)),
        (1j, (-1 + 1j, 1j, 1 + 1j)),
        (-1, (-1 - 1j, -1, -1 + 1j)),
        (1, (1 - 1j, 1, 1 + 1j)),
    ]
)

elves = []
for j, line in enumerate(lines):
    for i, char in enumerate(line):
        if char == "#":
            elves.append(complex(i, j))

rnd = 0
while True:
    rnd += 1
    no_go = set()
    prop_elves = {}
    for i, elf in enumerate(elves):
        if not any(elf + d in elves for d in ALL_DIRS):
            continue

        for d, view_dirs in dirs:
            if not any(elf + view_dir in elves for view_dir in view_dirs):
                nelf = elf + d
                if nelf in prop_elves:
                    no_go.add(nelf)
                else:
                    prop_elves[nelf] = i
                break

    move_elves = set(prop_elves) - no_go
    if not move_elves:
        break
    for prop_elf in move_elves:
        i = prop_elves[prop_elf]
        elves[i] = prop_elf

    dirs.rotate(-1)

print(rnd)
print("Execution time: ", datetime.now() - start_time)
