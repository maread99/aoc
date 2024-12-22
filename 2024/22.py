"""Day 22 Monkey Market:

That was a relief after yesterday...

part a: 18mins
Bit slow on the coding it up

part b: 55mins
Wasted at least ten minutes looking for a bug that didn't exist when I was
comparing answers for the part a example input with the part b example
answers.

total: 1hr 13mins, 6x bottom of the leaderboard.

7sec execution on my machine.

#counter  #generator
"""

import itertools
from collections import Counter
from aocd import get_data


raw = get_data(day=22, year=2024)

# raw = """1
# 10
# 100
# 2024
# """

MOD = 16777216

nums = [int(l) for l in raw.splitlines()]


def get_nxt(v):
    v = (((v * 64) ^ v)) % MOD
    v = ((v // 32) ^ v) % MOD
    return ((v * 2048) ^ v) % MOD


tot = 0
for n in nums:
    for _ in range(2000):
        n = get_nxt(n)
    tot += n

print(tot)

# part b

# raw = """1
# 2
# 3
# 2024
# """


def get_nxt_digit(v):
    yield v % 10
    for _ in range(2000):
        v = get_nxt(v)
        yield v % 10


CNT = Counter()
for n in nums:
    diffs = []
    cnt = Counter()
    for i, (a, b) in enumerate(itertools.pairwise(get_nxt_digit(n))):
        diffs.append(b - a)
        if i < 3:
            continue
        key = tuple(diffs[-4:])
        if key in cnt:
            continue
        cnt[key] = b
    CNT += cnt

print(CNT.most_common(1)[0][1])
