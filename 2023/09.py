"""Day 9: Mirage Maintenance

part a: 30mins.
    Around 10mins debugging. Carelessly introduced a bug by evaluating if
    a list contains all 0's with `not sum(line)`. Worked with the
    example 😏.

part b: 8mins
total: 38mins, 7x bottom of the leaderboard.

#arrays
"""

from aocd import get_data

raw = get_data(day=9, year=2023)

lines = [list(map(int, line_.split())) for line_ in raw.splitlines()]

# lines = """0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45
# """.splitlines()

# part a

cum = 0

for line in lines:
    srss = [line]
    # bug: Careless initial implementation...
    # while not sum(line):
    while line.count(0) != len(line):  # corrected
        line = [v - line[i] for i, v in enumerate(line[1:])]
        srss.append(line)

    srss = list(reversed(srss))
    extras = [0]
    for i, row in enumerate(srss[1:]):
        extras.append(extras[i] + row[-1])

    cum += extras[-1]

print(cum)

# part b
# same as part a save for a single line

cum = 0

for line in lines:
    srss = [line]
    while line.count(0) != len(line):
        line = [v - line[i] for i, v in enumerate(line[1:])]
        srss.append(line)

    srss = list(reversed(srss))
    extras = [0]
    for i, row in enumerate(srss[1:]):
        extras.append(row[0] - extras[i])  # only line changed from part a

    cum += extras[-1]

print(cum)
