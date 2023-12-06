"""Day 21: Monkey Math

part b, Trial and Error after interogating how the two values change for changes in
'humn' and seeing that one side is constant. To 'home in' used a helper that returned
difference for each digit. Changed 'humn' to reduce the difference for each digit to
zero. Didn't write a script for it.
EDIT - The way to do this was to identify from the pattern of outcomes that
the underlying function was monotonic and hence that the answer could be
homed in on via a binary search.
"""

import re

from aocd import get_data


raw = get_data(day=21, year=2022)
lines = raw.splitlines()


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


ms = {}
for line in lines:
    k, v = line.split(":")
    if vi := ints(v):
        ms[k] = vi[0]
    else:
        ms[k] = v.strip()

while not all(isinstance(v, (int, float)) for v in ms.values()):
    for k, v in ms.items():
        if isinstance(v, (int, float)):
            continue
        a, op, b = v.split()
        av, bv = ms[a], ms[b]
        if isinstance(av, (int, float)) and isinstance(bv, (int, float)):
            ms[k] = eval(f"{av}{op}{bv}")

print(int(ms["root"]))

# part b
ms = {}
for line in lines:
    k, v = line.split(":")
    if vi := ints(v):
        ms[k] = vi[0]
    else:
        ms[k] = v.strip()

ms["humn"] = 3_327_575_724_809  # by Trial and Error

while not all(isinstance(v, (int, float)) for v in ms.values()):
    for k, v in ms.items():
        if isinstance(v, (int, float)):
            continue
        a, op, b = v.split()
        av, bv = ms[a], ms[b]
        if isinstance(av, (int, float)) and isinstance(bv, (int, float)):
            ms[k] = eval(f"{av}{op}{bv}")

# print difference digit for digit
print([int(a) - int(b) for a, b in zip(str(ms["mrnz"]), str(ms["jwrp"])) if a != "."])
print(ms["humn"])
