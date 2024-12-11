"""Day 11: Plutonian Pebbles

I initially tried to solve this problem using recursion and spent an
embarrassingly long time getting to nowhere near how it should be done.
This solution draws heavily from @mebeim which IS how it should be done.
    https://github.com/mebeim/aoc/tree/master/2024#day-11---plutonian-pebbles

I struggle to get my head around recursion sufficiently that even when I
see a solution I still have no intuitve feel for how it works. This one
might be thought of a tree starting at the integer on a single stone and
branching from there, either a single branch to another number or two
branches to two numbers (if the number is such that two stones are
generated). At the end of 25 (part a) levels of branching, the end of each
branch returns 1, with each of these 1 representing a single stone at the
end. The 1s accumulate as it works back from the end of the branches to
the root and the initial call retuns how many terminations there were (i.e.
how many stones there were at the end).

Recursion alone would take forever. What's also necessary here is a cache
to ensure that no 'exact same' calculation is repeated. What's unique in
this case is a combination of a stone's value and the number of iterations
left until the end. Same value for the same number of iterations, going to
get back the same result. So just cache the result against a key of (value,
iterations_remaining) (or perhaps less intelligibly (value,
iterations_undertaken), which is the same difference as we're just
concerned with marking a level along the tree).

#recursion  #memoization  #codify-rules
"""

import functools

from aocd import get_data

raw = get_data(day=11, year=2024)

# raw = "125 17"


def get_stones(v) -> list[int] | list[int, int]:
    s = str(v)
    if v == 0:
        return [1]
    elif len(s) % 2:
        return [v * 2024]
    else:
        stop = len(s) // 2
        return [int(s[:stop]), int(s[stop:])]


@functools.cache
def num_stones(v: int, its: int) -> int:
    """Return final number of stones.

    Returns final number of stones if blink `its` more times and start with
    a single stone of value `v`.
    """
    if its == 0:
        return 1

    new_stones = get_stones(v)
    res = 0
    for ns in new_stones:
        res += num_stones(ns, its - 1)
    return res


vals = [int(v) for v in raw.split()]
print(sum(num_stones(v, 25) for v in vals))
print(sum(num_stones(v, 75) for v in vals))
