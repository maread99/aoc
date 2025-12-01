"""Day 1: Secret Entrance

NOTE: See 01rev.py for a much improved implementation. This version is
unnecessarily complicated as it fails to take advantage of the behaviour
of the modulus operator on negative numbers in Python.

part a: 21mins
My programming's got a bit of rust on it. Also misread the question
when scanning it, interpreting 'the number of times the dial is left
pointing at 0' as the "number of times the dial is pointing at 0 after
rotating 'left'" 🙄. Then failed to wrap dial from 100 to 0 if would
otherwise end on 100.

part b: 26mins
Initially was adding an extra 1 when dial started on 0 and turned left.

total: 47mins
10250
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
    if lr == "L":
        v -= n
        if v < 0:
            v = 100 - (abs(v) % 100)
            if v == 100:
                v = 0
    else:
        v += n
        if v > 99:
            v = 0 + v % 100
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
        v -= n
        if v <= 0:
            d, m = divmod(abs(v), 100)
            total += d + (0 if was0 else 1)
            v = 100 - m
            if v == 100:
                v = 0
    else:
        v += n
        if v > 99:
            d, m = divmod(v, 100)
            total += d
            v = 0 + m

print(total)
