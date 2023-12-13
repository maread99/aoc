"""Day 13: Point of Incidence

Incorporates the following features that were lacking in the original
solution:
    A simple transpose to evaluate vertical symmetry.

    Uses side effec to zip to ensure the same number of rows are being
    compared on either side of the mirror.

    For part b, finds the difference rather than the new reflection.

Wrote after seeing various solutions including:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day13p2.py

#arrays  #zip
"""

from aocd import get_data

raw = get_data(day=13, year=2023)

# raw = """#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#
# """

pats = raw.split("\n\n")

# part a


def get_pat_value(rows: list[str]) -> int:
    for i in range(1, len(rows)):
        above = rows[:i][::-1]
        below = rows[i:]

        for a, b in zip(above, below):
            if a != b:
                break
        else:
            return i
    return 0


total = 0
for pat in pats:
    rows = [list(row) for row in pat.splitlines()]
    total += get_pat_value(rows) * 100
    cols = list(zip(*rows))
    total += get_pat_value(cols)

print(total)

# part b


def get_pat_value(rows: list[str]) -> int:
    for i in range(1, len(rows)):
        above = rows[:i][::-1]
        below = rows[i:]

        # compare contents in mirrored rows
        diffs = 0
        for a, b in zip(above, below):
            for x, y in zip(a, b):
                if x != y:
                    diffs += 1
            if diffs > 1:
                break
        if diffs == 1:
            return i
    return 0


total = 0
for pat in pats:
    rows = [list(row) for row in pat.splitlines()]
    total += get_pat_value(rows) * 100
    cols = list(zip(*rows))
    total += get_pat_value(cols)

print(total)
