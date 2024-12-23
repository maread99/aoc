"""Day 21: Keypad Conundrum

part a: > 7 hours
part b: a fair few hours more.
total: Many hours.

I spent the best part of 45 minutes before I wrote a single character of
code. Realised that the path between two buttons that minimises the final
count will not always be the same, but rather depends on the current
position of the controlling robot. Then convinced myself this wasn't the
case and spent ages barking up the wrong tree. Didn't come back to
accepting the needed to use a BFS until after two and a half hours and then
ran into hours of countless careless bugs that were cropping up as a result
of making so many changes. Finally got part a out with a solution that
evaluated all the possible outcomes and took the shortest of them - an
implementation that was never going to work for part b.

Came back to part b after a couple of days and, with the benefit of having
reflected on the problem, actually didn't take too long to come up with
this recursive solution.

Only consolation here was actually having got it out.

#BFS  #recursion
"""

import functools
import itertools
import math
from collections import deque

from aocd import get_data


raw = get_data(day=21, year=2024)

# raw = """029A
# 980A
# 179A
# 456A
# 379A
# """

codes = raw.splitlines()

PADS = [
    [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]],
    [["#", "^", "A"], ["<", "v", ">"]],
]

PADS_MAP = {"num": PADS[0], "dir": PADS[1]}

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
VECS = (UP, DOWN, LEFT, RIGHT)

VEC_MAP = {
    UP: "^",
    DOWN: "v",
    LEFT: "<",
    RIGHT: ">",
}


def get_paths(pad, frm, to):
    if frm == to:
        return ("",)
    PAD = PADS_MAP[pad]

    for j, row in enumerate(PAD):
        for i, c in enumerate(row):
            if c == frm:
                S = (i, j)
                break
        else:
            continue
        break

    paths = []
    queue = deque([(S, "")])  # state as loc, path
    min_len = math.inf
    while queue:
        loc, path = queue.popleft()
        if len(path) >= min_len:
            continue
        for v in VECS:
            ni, nj = loc[0] + v[0], loc[1] + v[1]
            if ni < 0 or ni >= len(PAD[0]) or nj < 0 or nj >= len(PAD):
                continue
            nv = PAD[nj][ni]
            if nv == "#":
                continue
            npath = path + VEC_MAP[v]
            if nv == to:
                min_len = min(min_len, len(npath))
                paths.append(npath)
                continue
            queue.append(((ni, nj), npath))
    return tuple(paths)


@functools.cache
def get_next_buts_optns(buts, pad="dir"):
    opts = []
    for frm, to in itertools.pairwise("A" + buts):
        opts.append(get_paths(pad, frm, to))
    if not opts:
        return ("",)
    return tuple(itertools.product(*opts))


@functools.cache
def count(buts, i):
    if not i:
        return len(buts)
    next_opts = get_next_buts_optns(buts)
    counts = []
    for opt in next_opts:
        counts.append(sum(count(buts + "A", i - 1) for buts in opt))
    return min(counts)


tota = totb = 0
for code in codes:
    optns = get_next_buts_optns(code, pad="num")
    counts_a, counts_b = [], []
    for opt in optns:
        counts_a.append(sum(count(buts + "A", 2) for buts in opt))
        counts_b.append(sum(count(buts + "A", 25) for buts in opt))

    tota += min(counts_a) * int(code[:-1])
    totb += min(counts_b) * int(code[:-1])

print(tota)
print(totb)
