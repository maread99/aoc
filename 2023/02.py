"""Day 2: Cube Conundrum

part a: 32mins.
Reasons for debugging:
    Games were 1-indexed, not 0!
    'old' variable name unwittingly remained within the code.
        RESET INTERACTIVE ENVIRONMENTS! Or don't use one.

part b: 15mins
total: 47mins, 7.5x bottom of the leaderboard.
"""

from collections import defaultdict
from functools import reduce
import operator

from aocd import get_data

raw = get_data(day=2, year=2023)

lines = raw.splitlines()

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

# part a

total = 0
for i, game in enumerate(lines):
    invalid = False
    infos = game.strip().split(":")[1].strip().split(";")
    for info in infos:
        for cube in info.strip().split(","):
            num, color = cube.strip().split()
            assert color in limits
            limit = limits[color]
            if limit < int(num):
                invalid = True
                break
        if invalid:
            break
    else:
        total += i + 1

print(total)

# part b

total = 0
for i, game in enumerate(lines):
    infos = game.strip().split(":")[1].strip().split(";")
    maxs = defaultdict(int)
    for info in infos:
        for cube in info.split(","):
            num, color = cube.split()
            num = int(num)
            if num > maxs[color]:
                maxs[color] = num
    total += reduce(operator.mul, maxs.values())

print(total)
