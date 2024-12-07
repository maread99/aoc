"""Day 7: Bridge Repair

part a: 35mins
I messed around for a while with permutations and combinations of the
operators before realising that I was after a product with repetition.

part b: 19mins
Long execution time of 1min 40secs. I assumed that an optimisation of my
part_a solution would be required and so ditched using `functools.reduce`
in favour of a custom reduce which breaks whenever the total exceeds the
sought result. However, this actually makes no meaningful difference
to the execution time - I could have got the answer out much quicker by
just using reduce again and letting it run.

total: 54mins, 14.3x bottom of the leaderboard.

A simple optimisation is to append the lines that fail part_a to a list and
then only check these in part_b (then adding back the total from part_a).
However, I found it only saved about 7 seconds, not really significant
given the total execution time here. I originally solved without this
optimisation and haven't included it here.

Clearly, there has to be a way to solve this puzzle with a much quicker
execution...

#reduce #product #brute-force
"""

import functools
import itertools
import math
from aocd import get_data

raw = get_data(day=7, year=2024)

raw = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

lines_raw = raw.splitlines()
lines = []
for line in lines_raw:
    res_, values_ = line.split(":")
    res = int(res_)
    values = list(map(int, values_.strip().split()))
    lines.append((res, values))


total_a = 0
for res, values in lines:
    prods = itertools.product([sum, math.prod], repeat=len(values))
    for p in prods:
        g = (f for f in p)
        total = functools.reduce(lambda *vals: next(g)(vals), values)
        if total == res:
            total_a += total
            break
print(total_a)


def combine(vals):
    return int(str(vals[0]) + str(vals[1]))


total = 0
for res, values in lines:
    prods = itertools.product([sum, math.prod, combine], repeat=len(values))
    for p in prods:
        cum = values[0]
        for f, b in zip(p, values[1:]):
            cum = f([cum, b])
            if cum > res:
                break
        if cum == res:
            total += cum
            break
print(total)
