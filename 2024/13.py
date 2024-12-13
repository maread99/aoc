"""Day 13: Claw Contraption

I've used a combined solution on this one because I don't think it makes it
any less intelligle.

part a: 28mins
I solved with the brute-force solution commented out at the bottom of the
script.

part b: 66mins
Well brute force wasn't going to do it. My initial thoughts turned to it
being a lowest common multiple problem and I tried using the initial brute
force approach to hit x and y prize values that were factors of the
required prize values (and where the required prize values were the same
multiple of those factors). Too much brute force required and I guessed
that trying to optimise it was not how it was intended this problem be
solved.

Looked at the maths of what was required and realised it was a simple
matter of solving simultaneous equations.

Py = i.Ya + j.Yb
Px = i.Xa + j.Xb
rearranging to put both in terms of i:
i = (Py - j.Yb) / Ya
i = (Px - j.Xb) / Xa
and equating...
(Py - j.Yb) / Ya = (Px - j.Xb) / Xa
and multipling both sides by each side's denominator...
(Py - j.Yb).Xa = (Px - j.Xb).Ya
multiplying out:
Py.Xa - j.Yb.Xa = Px.Ya - j.Xb.Ya
rearranging to like terms...
j.Xb.Ya - j.Yb.Xa = Px.Ya - Py.Xa
j.(Xb.Ya - Yb.Xa) = Px.Ya - Py.Xa
and finally to get j:
j = (Px.Ya - Py.Xa) / (Xb.Ya - Yb.Xa)   # As in the code

i is solved by simply rearranging one of the original equations:
Py = i.Ya + j.Yb
i.Ya = Py - j.Yb
i = (Py - j.Yb) / Ya  # As in the code
...to which can sub in the now known value of j

total: 1hour 34mins, 8.5x bottom of the leaderboard.
Shame I didn't recognise it as a linear algebra problem earlier, although
happy enough.

#linear-algebra
"""

import re
from aocd import get_data

raw = get_data(day=13, year=2024)

# raw = """Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450

# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279
# """

blocks = raw.split("\n\n")
machines = []
for blk in blocks:
    machines.append([list(map(int, re.findall(r"\d+", l))) for l in blk.splitlines()])

ERROR = 10000000000000


def solve(part_b=False):
    tot = 0
    for (xa, ya), (xb, yb), (xp, yp) in machines:
        if part_b:
            xp += ERROR
            yp += ERROR
        j = (xp * ya - yp * xa) / (xb * ya - yb * xa)  # see module doc
        i = (yp - yb * j) / ya
        if j % 1 or i % 1:
            continue  # not being solved by a whole number of clicks
        tot += (i * 3) + j
    return int(tot)


print(solve())
print(solve(part_b=True))


# brute-force solution that I actually used for part a, 15secs to solve part a
# tot = 0
# for (xa, ya), (xb, yb), (xp, yp) in values:
#     res = []
#     max_ = max(xp // xa, xp // xb, yp // ya, yp // yb) + 1
#     for i in range(max_):
#         for j in range(max_):
#             if (i * xa) + (j * xb) == xp and (i * ya) + (j * yb) == yp:
#                 res.append(i*3 + j)
#     if res:
#         tot += min(res)
# print(tot)
