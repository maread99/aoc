"""Day 19: Linen Layout

Alternative version employing recursion for both a and b.

I can't believe how long it took me (over four and a half hours) to end up
with less than 15 lines of code.

#recursion  #memoization
"""

import functools
from aocd import get_data

raw = get_data(day=19, year=2024)

# raw = """r, wr, b, g, bwu, rb, gb, br

# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb
# """

top, bot = raw.split("\n\n")
TOWELS = set(top.split(", "))
dsgns = bot.splitlines()


@functools.cache
def ways(d):
    if not d:
        return 1
    return sum(ways(d[len(twl) :]) for twl in TOWELS if d.startswith(twl))


print(sum(1 for d in dsgns if ways(d)))
print(sum(ways(d) for d in dsgns))
