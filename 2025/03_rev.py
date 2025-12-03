"""Day 3: Lobby

How it should have been done. Part 1 is a simpler version of my original
solve. Part 2 is a generalisation of part 1 which could solve for any
number of batteries.

#iteration  #max
"""

from aocd import get_data

raw = get_data(day=3, year=2025)

# raw = """987654321111111
# 811111111111119
# 234234234234278
# 818181911112111
# """

lines = raw.splitlines()

# part 1
total = 0
for line in lines:
    bank = list(line)
    max1 = max(bank[:-1])
    idx = bank.index(max1)
    rem = bank[idx + 1 :]
    max2 = max(rem)
    total += int("".join((max1, max2)))

print(total)

# part 2
total = 0
for line in lines:
    rem = list(line)
    digits = ""
    for i in reversed(range(12)):
        digits += max(rem[: (-i if i else None)])
        idx = rem.index(digits[-1])
        rem = rem[idx + 1 :]
    total += int(digits)

print(total)
