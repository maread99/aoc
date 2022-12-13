"""Day 13: Distress Signal

As is common, hyper-neutrino had one of the most succient solutions out
there:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day13p1.py 
It shows how there's no need to consider equality as a separate state
(which I'd originally used None to describe). Can simply work with the 0
value.

This version defines a function that returns an interger to describe the
relationship between two pairs, as -1, 0, or 1. This is then employed as
the sort key in part b.

Also employs pattern matching.
"""

import ast
import functools

from aocd import get_data

eval = ast.literal_eval

raw = get_data(day=13, year=2022)


def cmpr(a: int | list[int], b: int | list[int]) -> int:
    match a, b:
        case int(), int():
            d = a - b
            return 0 if not d else d // abs(d)
        case int(), list():
            return cmpr([a], b)
        case list(), int():
            return cmpr(a, [b])

    for a_, b_ in zip(a, b):
        if d := cmpr(a_, b_):
            return d // abs(d)

    # tie
    d = len(a) - len(b)
    return 0 if not d else d // abs(d)


data = [[eval(p) for p in pair.splitlines()] for pair in raw.split("\n\n")]
t = 0
for i, (a, b) in enumerate(data):
    t += i + 1 if cmpr(a, b) < 0 else 0
print(t)

# part b

data = list(map(eval, raw.replace("\n\n", "\n").splitlines()))
markers = [[[2]], [[6]]]
data += markers

rtrn = sorted(data, key=functools.cmp_to_key(cmpr))
print((rtrn.index(markers[0]) + 1) * (rtrn.index(markers[1]) + 1))
