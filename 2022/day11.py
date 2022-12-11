"""Day 11: Monkey In The Middle.

Part a an hour, part b hours (between looking at the screen and ruminating
on it elsewhere). Solved by trying what seemed plausible rather than
through any conviction - suspected that the itegrity of the worry level
would be upheld if reset to the remainder left after dividing it by
the product of all the divisors.

EDIT - looks like this is the way to do it. It's effectively 'reducing
worry level' to the remainder after dividing by the least common multiple
of all the divisors. Could have used `math.lcm` (as rev version) which
would have reduced the combined divisor if any of the divisors were to have
been factors of any other. Following reference covers why this works in
the circumstances here as "the divisibility is preserved since congruence
to a fixed modulus is preserved by addition and multiplication, which are
the only two operations we perform", i.e. given the ops on the worry
level, its integrity is preserved when divided by the LCM.
    https://github.com/mebeim/aoc/tree/master/2022#day-11---monkey-in-the-middle
"""

import math
import re

from aocd import get_data

raw = get_data(day=11, year=2022)


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", s)))


data = raw.splitlines()
data = [data[i : i + 6] for i in range(0, len(data), 7)]


def get_monkeys() -> list[dict]:
    ms = [{} for _ in range(len(data))]
    for i, m_data in enumerate(data):
        d = ms[i]
        d["items"] = ints(m_data[1])
        d["op"] = "".join(m_data[2].split()[-2:])
        d["divisor"] = ints(m_data[3])[0]
        d["receivers"] = int(m_data[4].split()[-1]), int(m_data[5].split()[-1])
    return ms


ms = get_monkeys()


def turn(m: dict):
    for _ in range(len(m["items"])):
        old = m["items"][0]
        wl = eval(f"old{m['op']}") // 3
        receiver = m["receivers"][bool(wl % m["divisor"])]
        ms[receiver]["items"].append(wl)
        del m["items"][0]


times = [0] * len(ms)
for _ in range(20):
    for i, m in enumerate(ms):
        times[i] += len(m["items"])
        turn(m)

print(math.prod(sorted(times)[-2:]))

# part b

ms = get_monkeys()

divisors = [m["divisor"] for m in ms]
FAC = math.prod(divisors)


def turn(m: dict):
    for _ in range(len(m["items"])):
        old = m["items"][0]
        wl = eval(f"old{m['op']}")
        receiver = m["receivers"][bool(wl % m["divisor"])]
        wl = wl if wl <= FAC else wl % FAC
        ms[receiver]["items"].append(wl)
        del m["items"][0]


times = [0] * len(ms)
for _ in range(10000):
    for i, m in enumerate(ms):
        times[i] += len(m["items"])
        turn(m)

print(math.prod(sorted(times)[-2:]))
