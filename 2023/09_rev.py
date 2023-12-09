"""Day 9: Mirage Maintenance

Recursion offers a cleaner implementation.

#recursion
"""

import itertools

from aocd import get_data

raw = get_data(day=9, year=2023)

# raw = """0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45
# """

lines = [list(map(int, line_.split())) for line_ in raw.splitlines()]

# part a


def get_next_value(line: list[int]) -> int:
    if line.count(0) == len(line):
        return 0

    next_line = [b - a for a, b in itertools.pairwise(line)]
    return line[-1] + get_next_value(next_line)


print(sum(get_next_value(line) for line in lines))


# part b


def get_prev_value(line: list[int]) -> int:
    if line.count(0) == len(line):
        return 0

    next_line = [b - a for a, b in itertools.pairwise(line)]
    return line[0] - get_prev_value(next_line)


print(sum(get_prev_value(line) for line in lines))
