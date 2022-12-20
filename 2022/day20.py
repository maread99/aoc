"""Day 20: Grove Positioning System

Messed around trying to change a list in place. Got it working for part a
although same approach for part b seems to fall apart on encountering an
edge case (the example goes out of kilter from around the 3rd mixing).

On which, only got part a out, and probably more due to luck with the data
than a decent implementation.
"""

import itertools
import re

from aocd import get_data

raw = get_data(day=20, year=2022)

# raw = """1
# 2
# -3
# 3
# -2
# 0
# 4"""

lines = raw.splitlines()


def first_int(s: str) -> int:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))[0]


nums = list(map(first_int, lines))

LEN = len(nums)


def get_new_index(i, num):
    if num == 0:
        return i
    ni = i + num
    if ni < 0:
        return LEN - (abs(ni) % (LEN - 1))
    if ni > LEN - 1:
        ni = ni % (LEN - 1)

    ni += 1 if ni > i else 0

    # if ni == LEN - 1:
    #     return 0
    # if ni == 0:
    #     return LEN
    return ni


idx_num = list(enumerate(nums))

seq = iter(idx_num.copy())

i_ = 0
while nxt := next(seq, False):
    i = idx_num.index(nxt)
    ni = get_new_index(i, nxt[1])
    idx_num.insert(ni, nxt)
    if ni < i:
        i += 1
    del idx_num[i]

lst = [t[1] for t in idx_num]
itr = itertools.cycle(lst)
i = lst.index(0)

for _ in range(i + 1):
    next(itr)

a = []
for i in range(1, 3001):
    v = next(itr)
    if i in (1000, 2000, 3000):
        a.append(v)

print(sum(a))


CONST = 811589153
idx_num = [(i, num * CONST) for i, num in enumerate(nums)]

seq = iter(idx_num.copy() * 10)

i_ = 0
while nxt := next(seq, False):
    i = idx_num.index(nxt)
    ni = get_new_index(i, nxt[1])
    idx_num.insert(ni, nxt)
    if ni < i:
        i += 1
    del idx_num[i]

lst = [t[1] for t in idx_num]
itr = itertools.cycle(lst)
i = lst.index(0)

for _ in range(i + 1):
    next(itr)

b = []
for i in range(1, 3001):
    v = next(itr)
    if i in (1000, 2000, 3000):
        b.append(v)

print(sum(b))
