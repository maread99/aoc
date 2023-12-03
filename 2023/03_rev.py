"""Day 3: Gear Ratios

Wrote this after seeing this gem:
https://github.com/iKevinY/advent/blob/main/2023/day03.py

Tackles the problem from a simpler angle - uses tuples to record the
positions of each symbol and number gathered from a single walk-through.
Then, considers each symbol in turn. Can ignore bounds.

Lesson - rather than dive straight in with the first approach that occurs,
take some time to consider all the options and identify the simplest.
"""

from collections import defaultdict
import math

from aocd import get_data

raw = get_data(day=3, year=2023)

lines = raw.splitlines()

# create GRID

SYMBOLS: list[tuple[int, int, str]] = []  # where tuple [c, r, char]
# where key row where tuple [number, c_start, c_end]...
PARTS: dict[int, list[tuple[int, int, int]]] = defaultdict(list)


# create symbols and parts

for r, row in enumerate(lines):
    num = ""
    for c, char in enumerate(row):
        if char != "." and not char.isdigit():
            SYMBOLS.append((c, r, char))
        if char.isdigit():
            if not num:
                start = c
            num += char
        elif num:
            PARTS[r].append((int(num), start, c - 1))
            num = ""
    if num:
        PARTS[r].append((int(num), start, c))

# parts a and b

total = 0
total_gears = 0
for c, r, symb in SYMBOLS:
    gears = []
    for numb, start, end in PARTS[r - 1] + PARTS[r] + PARTS[r + 1]:
        if start - 1 <= c <= end + 1:
            total += numb
            if symb == "*":
                gears.append(numb)
    if len(gears) == 2:
        total_gears += math.prod(gears)

print(total)
print(total_gears)
