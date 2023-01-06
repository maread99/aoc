"""Day 25: Full of Hot Air.

part a, few hours!

Got the base 10 sum out quick enough, although went barking up more than
one wrong tree from there, trying to brute force the conversion to snafu
(until realised the real input was up to 20 digits!), then trying to
evaluate it from the most significant digit first rather than the least.

Ended up working out how to sum it directly in SNAFU. See alt version for
evaluating in base 10 and converting back.
"""

from aocd import get_data

raw = get_data(day=25, year=2022)
lines = raw.splitlines()

LONGEST = max([len(line) for line in lines])
MAP = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
MAP_REV = {v: k for k, v in MAP.items()}

# least significant figure first and 0 padded to max length
snafus = [
    [MAP[char] for char in line[::-1]] + [0] * (LONGEST - len(line))
    for line in lines
]
ts = [sum(vs) for vs in zip(*snafus)]  # total for each column ignoring any carry over

out = ""
carry_over = co = 0
for t in ts:
    nco, r = divmod(t + co, 5)
    if r > 2:
        r -= 5
        nco += 1
    co = nco
    out = MAP_REV[r] + out

print(out)
