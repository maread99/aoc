"""Day 13: Distress Signal

I did not know you could pass a comparision function to sort's key
argument! (This is why I do aoc.)

Also uses `ast.literal_eval` for security:
    https://www.reddit.com/r/adventofcode/comments/zkoc0o/2022_day_13_got_some_weird_input_today_hope_none/
"""

import ast
import functools

from aocd import get_data

eval = ast.literal_eval

raw = get_data(day=13, year=2022)

data = [pair.splitlines() for pair in raw.split("\n\n")]


def in_order_(left: int | list[int], right: int | list[int]) -> bool | None:
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    for l_, r in zip(left, right):
        if isinstance(l_, int) and isinstance(r, int):
            if l_ == r:
                continue
            return l_ < r
        if isinstance(l_, int):
            l_ = [l_]
        if isinstance(r, int):
            r = [r]
        ordered = in_order_(l_, r)
        if ordered is not None:
            return ordered

    # tie
    if len(left) == len(right):
        return None
    return len(left) < len(right)


def in_order(left: int | list[int], right: int | list[int]) -> bool:
    ordered = in_order_(left, right)
    return True if ordered is None else ordered


t = 0
for i, pair in enumerate(data):
    t += i + 1 if in_order(eval(pair[0]), eval(pair[1])) else 0
print(t)

# part b

data = raw.replace("\n\n", "\n").splitlines()
markers = ["[[2]]", "[[6]]"]
data += markers


def cmp(a, b):
    if a == b:
        return 0
    if in_order(eval(a), eval(b)):
        return -1
    return 1


rtrn = sorted(data, key=functools.cmp_to_key(cmp))
print((rtrn.index(markers[0]) + 1) * (rtrn.index(markers[1]) + 1))
