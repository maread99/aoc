"""Day 19: Linen Layout

part a: 1hr 42mins
Lost a bit of time not realising that there were an unlimited number of
each towel available, although the main loss was not recognising it as a
search algo, which I only found my way to on trying to write up a solution.

See `19_alt.py` for an alternative, simpler, version that uses recursion
based on the part b solution here.

part b: 2hrs 53mins
Made a right meal of this one. I tried to adapt the part a search and was
failing to break the larger towels into smaller ones. Went recursion
and it all came out (although not until overcopmlicating it all by
thinking I needed to distinguish between divisible and indivisible towels
at the end of the design).

total: 4hrs 35mins, 85x bottom of a LLM-infeseted leaderboard, although
even still, would have been rubbish. I made a large mountain out of a mole
hill.

#DFS  #recursion  #memoization
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

# part a

n = 0
for dsn in dsgns:
    queue = [dsn]
    seen = set()
    while queue:
        d = queue.pop()
        if d in seen:
            continue
        else:
            seen.add(d)
        for twl in TOWELS:
            if d == twl:
                n += 1
                break
            if d.startswith(twl):
                queue.append((d[len(twl) :]))
        else:
            continue
        break
print(n)

# part b


@functools.cache
def ways(d):
    if not d:
        return 1
    return sum(ways(d[len(twl) :]) for twl in TOWELS if d.startswith(twl))


print(sum(ways(d) for d in dsgns))
