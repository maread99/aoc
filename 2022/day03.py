"""Day 3: Rucksack Reorganization"""

from aocd import get_data

raw = get_data(day=3, year=2022)

data = raw.split("\n")

OFFSET_UPPER = ord("A") - 27
OFFSET_LOWER = ord("a") - 1


def map_char(char: str) -> int:
    if char.upper() == char:
        return ord(char) - OFFSET_UPPER
    return ord(char) - OFFSET_LOWER


total = 0
for line in data:
    midpoint = len(line) // 2
    a, b = line[:midpoint], line[midpoint:]
    char = (set(a).intersection(set(b))).pop()
    total += map_char(char)
print(total)

total = 0
for i in range(0, len(data) - 2, 3):
    a, b, c = data[i:i + 3]
    char = (set(a).intersection(set(b)).intersection(set(c))).pop()
    total += map_char(char)
print(total)
