"""Day 6: Trash Compactor

part 1: 13mins

part 2: 50mins
If I spent 3 minutes reading and actually understanding the questions I'd
spend 30 minutes less solving them. I don't learn.

total: 64mins
12000
#zip
"""

import math

from aocd import get_data

# raw = get_data(day=6, year=2025)

raw = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

all_lines = raw.splitlines()
ops = [sum if op == "+" else math.prod for op in all_lines[-1].split()]

# part 1

lines = [list(map(int, line.split())) for line in all_lines[:-1]]
total = 0
for i, col in enumerate(zip(*lines)):
    total += ops[i](col)
print(total)


# part 2

total = 0
i = 0
vals = []
for col in zip(*all_lines[:-1]):
    v = "".join(col).strip()
    if not v:
        total += ops[i](vals)
        vals = []
        i += 1
        continue
    vals.append(int(v))

total += ops[-1](vals)  # don't forget the last one

print(total)
