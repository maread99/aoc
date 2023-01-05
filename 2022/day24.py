"""Day 24: Blizzard Basin.

part a, 4 hours
Initially went with a version where the depth-first search was not
constrained by a forced minimum (which the version below is). At about
15mins into the execution realised it would be quicker to force a minimum
to keep the search space down and keep raising that forced minimum until
the actual minimum is found (which will be the first iteration which
evaluates a lower minimum than the forced value). The unforced version
completed in 23mins, raising the forced minimum by one each iteration took
under 4 minutes, raising the foced minimum by 50 for each iteration took
around 8 seconds (version as below).

part b, 30 mins
"""

import math

from aocd import get_data
import numpy as np


raw = get_data(day=24, year=2022)
lines = raw.splitlines()

START = lines[0].index(".") + 0j
END = lines[-1].index(".") + (len(lines) - 1) * 1j

bN, bE, bS, bW, border = [], [], [], [], []
BLIZ_MAP = {"^": bN, ">": bE, "v": bS, "<": bW}
for j, line in enumerate(lines):
    for i, char in enumerate(line):
        pos = i + j * 1j
        if char in BLIZ_MAP:
            BLIZ_MAP[char].append(pos)
        if char == "#":
            border.append(pos)

MIN_ROW, MAX_ROW = 1j, (len(lines) - 2) * 1j
MIN_COL, MAX_COL = 1, len(lines[1]) - 2

border.append(START - 1j)  # add border behind entrance
border.append(END + 1j)  # add border behond exit
BORDER = np.array(border)
DIRS = [1, 1j, -1j, -1]

baNj = np.array([b - b.real for b in bN])
baNi = np.array([b.real for b in bN])
baEj = np.array([b - b.real for b in bE])
baEi = np.array([b.real for b in bE])
baSj = np.array([b - b.real for b in bS])
baSi = np.array([b.real for b in bS])
baWj = np.array([b - b.real for b in bW])
baWi = np.array([b.real for b in bW])

# There are only 600 versions of the grid (for real input). Store each version.
NUM_GRIDS = math.lcm(MAX_COL, int(MAX_ROW.imag))

# treat border as blizzard
bs = np.concatenate([baNi + baNj, baSi + baSj, baEi + baEj, baWi + baWj, BORDER])
BS = [bs]

for i in range(NUM_GRIDS):
    baNj -= 1j
    baNj[baNj == 0] = MAX_ROW
    baSj += 1j
    baSj[baSj == MAX_ROW + 1j] = MIN_ROW
    baEi += 1
    baEi[baEi == MAX_COL + 1] = MIN_COL
    baWi -= 1
    baWi[baWi == 0] = MAX_COL
    bs = np.concatenate([baNi + baNj, baSi + baSj, baEi + baEj, baWi + baWj, BORDER])
    BS.append(bs)

assert (BS[0] == BS[-1]).all()  # check it does repeat
del BS[-1]


ABS_MIN = (END.real - START.real) + (END.imag - START.imag)


def get_quickest(start=START, end=END, start_tm=0) -> int:
    min_ = start_tm + ABS_MIN - 1
    while True:
        min_ += 50
        start_min = min_

        paths = [(start, start_tm)]
        seen = {}
        while paths:
            pos, tm = paths.pop()

            # as the path length is shorter than the number of iterations, including
            # this modulus in the state has no benefit (although it was beneficial
            # when the min_ wasn't being forced).
            state = (pos, tm % NUM_GRIDS)
            if state in seen and seen[state] <= tm:
                continue
            seen[state] = tm

            tm += 1
            if tm >= min_:
                continue

            bs = BS[tm % NUM_GRIDS]
            nposs = [npos for d in DIRS if (npos := pos + d) not in bs]

            if not nposs and pos in bs:
                continue  # wiped out

            if end in nposs:
                min_ = min(min_, tm)
                continue

            if pos not in bs:  # could wait
                paths.append((pos, tm))
            for npos in nposs:
                paths.append((npos, tm))

        if min_ < start_min:
            break

    return int(min_)


FIRST_LEG = get_quickest()
print(FIRST_LEG)

SECOND_LEG = get_quickest(END, START, FIRST_LEG)
THIRD_LEG = get_quickest(START, END, SECOND_LEG)
print(THIRD_LEG)
