"""Day 23: Unstable Diffusion.

My original solution was pretty similar to hyper-neutrino's with one major
exception - my use of lists over sets. This revision puts into perspective
just how inefficient manipulating lists is compared to sets - what took
12mins is now taking less than 12 seconds!!
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day23p1.py

This implementation is otherwise the same as the original.

Initially I'd actually started to use sets although switched to lists on
seeing that using sets would necessitate doubling up on some querying - I
had no appreciation of how insignificant querying a set is compared to
manipulating a list.
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

elves = set()
for j, line in enumerate(lines):
    for i, char in enumerate(line):
        if char == "#":
            elves.add(complex(i, j))

for _ in range(10):
    once = set()
    twice = set()
    for elf in elves:
        if not any(elf + d in elves for d in ALL_DIRS):
            continue

        for d, view_dirs in dirs:
            if not any(elf + view_dir in elves for view_dir in view_dirs):
                nelf = elf + d
                if nelf in once:
                    twice.add(nelf)
                else:
                    once.add(nelf)
                break
    
    elves_copy = elves.copy()
    for elf in elves_copy:
        if not any(elf + d in elves_copy for d in ALL_DIRS):
            continue

        for d, view_dirs in dirs:
            if not any(elf + view_dir in elves_copy for view_dir in view_dirs):
                nelf = elf + d
                if nelf not in twice:
                    elves.remove(elf)
                    elves.add(nelf)
                break

    dirs.rotate(-1)

cs = max(elf.real for elf in elves) - min(elf.real for elf in elves) + 1
rs = max(elf.imag for elf in elves) - min(elf.imag for elf in elves) + 1
print(int((cs * rs) - len(elves)))

# # part b, same approach as part a, breaking now when no elves to move

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

elves = set()
for j, line in enumerate(lines):
    for i, char in enumerate(line):
        if char == "#":
            elves.add(complex(i, j))

rnd = 0
while True:
    rnd += 1
    once = set()
    twice = set()
    for elf in elves:
        if not any(elf + d in elves for d in ALL_DIRS):
            continue

        for d, view_dirs in dirs:
            if not any(elf + view_dir in elves for view_dir in view_dirs):
                nelf = elf + d
                if nelf in once:
                    twice.add(nelf)
                else:
                    once.add(nelf)
                break

    if not once:
        break

    elves_copy = elves.copy()
    for elf in elves_copy:
        if not any(elf + d in elves_copy for d in ALL_DIRS):
            continue

        for d, view_dirs in dirs:
            if not any(elf + view_dir in elves_copy for view_dir in view_dirs):
                nelf = elf + d
                if nelf not in twice:
                    elves.remove(elf)
                    elves.add(nelf)
                break

    dirs.rotate(-1)

print(rnd)
