"""Day 11: Reactor

How it should be done - FAR more simply than my initial solution.

#DFS #memoization
"""

from functools import cache

from aocd import get_data

# raw = """aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out
# """

# raw = """svr: aaa bbb
# aaa: fft
# fft: ccc
# bbb: tty
# tty: ccc
# ccc: ddd eee
# ddd: hub
# hub: fff
# eee: dac
# dac: fff
# fff: ggg hhh
# ggg: out
# hhh: out
# """

raw = get_data(day=11, year=2025)

lines = raw.splitlines()

NETWORK = {}
for line in lines:
    k, v = line.split(": ")
    NETWORK[k] = v.split()

@cache
def num_paths(frm: str, to: str) -> int:
    if frm == to:
        return 1
    return sum(num_paths(nxt, to) for nxt in NETWORK.get(frm, []))

print(num_paths("you", "out"))
print(num_paths("svr", "fft") * num_paths("fft", "dac") * num_paths("dac", "out"))
