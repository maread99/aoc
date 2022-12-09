"""Day 9: Rope Bridge

Alternative solution using complex numbers to represent coordinates.

Written after seeing:
    https://github.com/MasterMedo/aoc/blob/f0b1e07813ed75214f143add6d14de118f70fde9/2022/day/9.py
    https://github.com/viliampucik/adventofcode/blob/d06a3431247df00736c9fa0635b8cdf7199e869d/2022/09.py
"""

from aocd import get_data

raw = get_data(day=9, year=2022)

data = raw.splitlines()

VECS = {"U": 1j, "D": -1j, "L": -1, "R": 1}
knots = [0] * 10
a = {0}
b = {0}

for n, line in enumerate(data):
    direction, num = line.split()
    for _ in range(int(num)):
        knots[0] += VECS[direction]
        for i in range(len(knots)-1):
            diff = knots[i] - knots[i+1]
            x, y = diff.real, diff.imag
            if 2 in [abs(x), abs(y)]:
                # move tail
                dx = 0 if not x else x / abs(x)  # 0 or signed 1
                dy = 0 if not y else y / abs(y)  # 0 or signed 1
                knots[i+1] += complex(dx, dy)
        a.add(knots[1])
        b.add(knots[-1])

print(len(a))
print(len(b))
