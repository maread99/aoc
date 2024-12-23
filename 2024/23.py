"""Day 23: LAN Party

part a: 20mins
Silly misread cost me a bit.

A brute force approach. A more optimised solution similar to part b would
offer a quicker execution.

part b: 17mins

total: 37mins, 7.4x bottom of the leaderboard.

#sets  #combinations
"""

import itertools
from collections import defaultdict
from aocd import get_data


raw = get_data(day=23, year=2024)

# raw = """kh-tc
# qp-kh
# de-cg
# ka-co
# yn-aq
# qp-ub
# cg-tb
# vc-aq
# tb-ka
# wh-tc
# yn-cg
# kh-ub
# ta-co
# de-co
# tc-td
# tb-wq
# wh-td
# ta-ka
# td-qp
# aq-cg
# wq-ub
# ub-vc
# de-ta
# wq-aq
# wq-vc
# wh-yn
# ka-de
# kh-ta
# co-tc
# wh-qp
# tb-vc
# td-yn
# """

lines = raw.splitlines()

mp = defaultdict(set)
cmptrs = set()
for l in lines:
    a, b = l.split("-")
    mp[a].add(b)
    mp[b].add(a)
    cmptrs |= {a, b}

# part a

tot = 0
for a, b, c in itertools.combinations(cmptrs, 3):
    if b not in mp[a] or c not in mp[a] or c not in mp[b]:
        continue
    if "t" == a[0] or "t" == b[0] or "t" == c[0]:
        tot += 1

print(tot)

# part b

sts = []
max_len = 0
for l in lines:
    break_ = False
    a, b = l.split("-")
    others = mp[a] & mp[b]
    for oa, ob in itertools.combinations(others, 2):
        if not oa in mp[ob]:
            break
    else:
        st = {a, b} | others
        if len(st) < max_len:
            continue
        max_len = len(st)
        if st not in sts:
            sts.append(st)

res = next(st for st in sts if len(st) == max_len)
print(",".join(sorted(res)))
