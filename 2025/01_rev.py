"""Day 1: Secret Entrance

Tidier revised version.

#divmod
"""

from aocd import get_data

raw = get_data(day=1, year=2025)

# raw = """L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82
# """

v = 50
total = 0

lines = raw.splitlines()

# part 1
for line in lines:
    lr = line[0]
    n = int(line[1:])
    v = (v - n) % 100 if lr == "L" else (v + n) % 100
    if v == 0:
        total += 1

print(total)


# part 2
total = 0
v = 50

for line in lines:
    lr = line[0]
    n = int(line[1:])
    was0 = v == 0
    if lr == "L":
        d, v = divmod(v - n, 100)
        # -1 if was0 as moving 'from' 0 to 99 doesn't count
        total += (1 if v == 0 else 0) + abs(d) - (1 if was0 else 0)
    else:
        d, v = divmod(v + n, 100)
        total += d

print(total)
