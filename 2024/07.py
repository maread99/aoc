"""Day 7: Bridge Repair

part a: 35mins
I messed around for a while with permutations and combinations of the
operators before realising that I was after a product with repetition.

part b: 19mins
30 second execution time. (NB I've edited this file to correct the number
of repetitions when evaluating the products - I needed a minus 1 in there.
With the superfluous repetition execution was taking 1 minute 40 seconds!)

total: 54mins, 14.3x bottom of the leaderboard.

NOTE This solution is inefficient! A more efficient implementation is
recursion which avoids much of the computation duplication. I'll put up
a revised version.

#reduce #product #brute-force
"""

import functools
import itertools
import math
from aocd import get_data

raw = get_data(day=7, year=2024)

# raw = """190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20
# """

lines_raw = raw.splitlines()
lines = []
for line in lines_raw:
    res_, values_ = line.split(":")
    res = int(res_)
    values = list(map(int, values_.strip().split()))
    lines.append((res, values))


total_a = 0
failed_lines = []
for res, values in lines:
    failed = True
    prods = itertools.product([sum, math.prod], repeat=len(values) - 1)
    for p in prods:
        g = (f for f in p)
        total = functools.reduce(lambda *vals: next(g)(vals), values)
        if total == res:
            total_a += total
            failed = False
            break
    if failed:
        failed_lines.append((res, values))
print(total_a)


def combine(vals):
    return int(str(vals[0]) + str(vals[1]))


total_b = 0
for res, values in failed_lines:
    prods = itertools.product([sum, math.prod, combine], repeat=len(values) - 1)
    for p in prods:
        g = (f for f in p)
        total = functools.reduce(lambda *vals: next(g)(vals), values)
        if total == res:
            total_b += total
            break
print(total_b + total_a)


# part_b 'optimisation' which actully offers no improvement over the solution above.
# total = 0
# for res, values in lines:
#     prods = itertools.product([sum, math.prod, combine], repeat=len(values)-1)
#     for p in prods:
#         cum = values[0]
#         for f, b in zip(p, values[1:]):
#             cum = f([cum, b])
#             if cum > res:
#                 break  # fail early if exceed the required value
#         if cum == res:
#             total += cum
#             break
# print(total)
