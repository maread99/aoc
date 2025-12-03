"""Day 3: Lobby

part 1: 28mins
Again, read the question too quickly and went barking up the wrong tree
twice before realising what was actually being asked for (not a simple
sort or two and extracting from the end).

I then overcomplicated it. See '03_rev.py' for the way to do it.

part 2: 36mins
Approach could be used for part 1 by simply changing the two 12s for 2s.

total: 64mins

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

# part 1 (overcomplicated solve)
total = 0
for line in lines:
    h = ("0", -1)
    for i, c in enumerate(line[:-1]):
        if c > h[0]:
            h = (c, i)
    h2 = "0"
    rem = line[h[-1] + 1 :]
    for c in rem:
        if c > h2:
            h2 = c
    total += int("".join((h[0], h2)))

print(total)


# part 2
total = 0
for line in lines:
    # assume value as last 12 digits
    val = line[-12:]
    # for each prior digit in turn, consider all possible values and take
    # the highest
    for c in reversed(line[:-12]):
        vals = [int(val)]
        # each alternative will be the new digit to the left in place of
        # one of the existing digits (which would be dropped..)
        for i in range(len(val)):
            ns = c + val[:i] + val[i + 1 :]
            vals.append(int(ns))
        val = str(max(vals))
    total += int(val)

print(total)
