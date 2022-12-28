"""Day 20: Grove Positioning System

Took an age to get both parts of this one out, all due to not implementing
in a methodical manner and failing to fully appreciate the mechanics of
list manipulation in each of the various circumstances accounted for within
`solve`.

@oliver-ni offers a far neater solution that takes advantage of being able
to rotate through a deque:
    https://github.com/oliver-ni/advent-of-code/blob/master/py/2022/day20.py
"""

from collections.abc import Iterable
import itertools
import re

from aocd import get_data

raw = get_data(day=20, year=2022)

lines = raw.splitlines()


def first_int(s: str) -> int:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))[0]


nums = list(map(first_int, lines))
LEN = len(nums)


def solve(idx_num: list[tuple[int, int]], seq: Iterable[tuple[int, int]]):
    while nxt := next(seq, False):
        i = idx_num.index(nxt)
        num = nxt[1]
        if num == 0:
            continue
        ni = i + num
        v = idx_num.pop(i)
        if 0 <= ni <= (LEN - 1):
            if ni == 0:
                idx_num.append(v)
            elif ni == (LEN - 1):
                idx_num.insert(0, v)
            else:
                idx_num.insert(ni, v)
        elif ni < 0:
            ni = -(abs(ni) % (LEN - 1))
            if ni == 0:
                idx_num.append(v)
            else:
                idx_num.insert(ni, v)
        else:
            ni %= LEN - 1
            idx_num.insert(ni, v)

    lst = [t[1] for t in idx_num]
    itr = itertools.cycle(lst)
    i = lst.index(0)

    for _ in range(i + 1):
        next(itr)

    vs = []
    for i in range(1, 3001):
        v = next(itr)
        if i in (1000, 2000, 3000):
            vs.append(v)
    print(sum(vs))


idx_num = list(enumerate(nums))
seq = iter(idx_num.copy())
solve(idx_num, seq)

CONST = 811589153
idx_num = [(i, num * CONST) for i, num in enumerate(nums)]
seq = iter(idx_num.copy() * 10)
solve(idx_num, seq)
