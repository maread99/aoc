"""Day 11: Monkey In The Middle.

No major revisions, more of a tidy in light of a few things I picked up
when looking around:
    Use `math.lcm` to make what's going on more explicit and potentially
    more efficient.

    Cleaner to store 'op' as a lamba which does the operation.

    Tidy the initial creation of data - don't overcomplicate grouping when
    can simply split on what separates the groups!
    (here '\n\n').
"""

import math
import re

from aocd import get_data


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", s)))


raw = get_data(day=11, year=2022)
data = [m_data.splitlines() for m_data in raw.split("\n\n")]


def get_monkeys() -> list[dict]:
    ms = [{} for _ in range(len(data))]
    for i, m_data in enumerate(data):
        d = ms[i]
        d["items"] = ints(m_data[1])
        d["op"] = eval(f"lambda old: {''.join(m_data[2].split()[-3:])}")
        d["divisor"] = ints(m_data[3])[0]
        d["receivers"] = int(m_data[4].split()[-1]), int(m_data[5].split()[-1])
    return ms


ms = get_monkeys()


def turn(m: dict):
    for _ in range(len(m["items"])):
        wl = m["op"](m["items"][0]) // 3
        receiver = m["receivers"][bool(wl % m["divisor"])]
        ms[receiver]["items"].append(wl)
        del m["items"][0]


counts = [0] * len(ms)
for _ in range(20):
    for i, m in enumerate(ms):
        counts[i] += len(m["items"])
        turn(m)

print(math.prod(sorted(counts)[-2:]))

# part b

ms = get_monkeys()

LCM = math.lcm(*[m["divisor"] for m in ms])


def turn(m: dict):
    for _ in range(len(m["items"])):
        wl = m["op"](m["items"][0]) % LCM
        receiver = m["receivers"][bool(wl % m["divisor"])]
        ms[receiver]["items"].append(wl)
        del m["items"][0]


counts = [0] * len(ms)
for _ in range(10000):
    for i, m in enumerate(ms):
        counts[i] += len(m["items"])
        turn(m)

print(math.prod(sorted(counts)[-2:]))
