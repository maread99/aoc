"""Day 25: Full of Hot Air.

Alternative summing in base 10 and converting result back to SNAFU.

Inspired by:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day25.py
    https://github.com/viliampucik/adventofcode/blob/master/2022/25.py
The latter is the shorter version, although the +2 is a bit too much of a
leap for me in terms of inteligibility, prefer baby steps.
"""

from aocd import get_data

raw = get_data(day=25, year=2022)
lines = raw.splitlines()

t = 0
for line in lines:
    t += sum(5**i * ("=-012".index(x) - 2) for i, x in enumerate(line[::-1]))

out = ""
while t:
    t, r = divmod(t, 5)
    if r > 2:
        t += 1
    out = "012=-"[r] + out

print(out)
