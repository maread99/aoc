"""Day 7: Bridge Repair

This more efficient solution uses recursion.

Inspired by jonathanpaulson (and others):
    https://github.com/jonathanpaulson/AdventOfCode/blob/master/2024/7.py

#recursion #brute-force

Alternatives
------------
For an even quicker implementation check out hyper-neutrino's solve:
    https://github.com/hyperneutrino/advent-of-code/blob/main/2024/day07p2.py
    (video) https://www.youtube.com/watch?v=1ZIJ9qo9bnY
This works backwards and discards paths where the 'last' operand cannot
feasibly result in the target value being met (with that target value being
revised with each step back through the list of operands).
"""

from aocd import get_data

raw = get_data(day=7, year=2024)

# raw = """190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20
# """

lines_raw = raw.splitlines()
lines = []
for line in lines_raw:
    res_, values_ = line.split(":")
    res = int(res_)
    values = list(map(int, values_.strip().split()))
    lines.append((res, values))


def as_result(res: int, cum: int, values: list[int]) -> bool:
    if not values:
        return res == cum
    nv = values[0]
    for ncum in (cum + nv, cum * nv):
        if as_result(res, ncum, values[1:]):
            return True
    return False


total = 0
for res, values in lines:
    total += res if as_result(res, values[0], values[1:]) else 0

print(total)


def as_result(res: int, cum: int, values: list[int]) -> bool:
    if not values:
        return res == cum
    nv = values[0]
    for ncum in (cum + nv, cum * nv, int(str(cum) + str(nv))):
        if as_result(res, ncum, values[1:]):
            return True
    return False


total = 0
for res, values in lines:
    total += res if as_result(res, values[0], values[1:]) else 0
print(total)
