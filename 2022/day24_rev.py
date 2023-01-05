"""Day 24: Blizzard Basin.

Original solution completely overengineered this by forcing a depth-first
search on a shortest-path problem rather than employing the vastly more
appropriate breadth-first search (given the equal weights of all edges).
Having used dfs for recent problems I just lept for it again without
thinking what I was after here!

This revision changes from dfs to bfs, otherwise as original.
Implementation significantly simplified by only requiring a single
iteration which always runs along 'minimum' paths until finds the end.
Execution time reduced from 20s to 8s.
"""

from collections import deque
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


def get_quickest(start=START, end=END, start_tm=0) -> int:
    q = deque([(start, start_tm)])
    seen = set()
    while q:
        state = q.popleft()

        if state in seen:
            continue
        seen.add(state)

        pos, tm = state
        tm += 1

        bs = BS[tm % NUM_GRIDS]
        nposs = [npos for d in DIRS if (npos := pos + d) not in bs]

        if not nposs and pos in bs:
            continue  # wiped out

        if end in nposs:
            break

        if pos not in bs:  # could wait
            q.append((pos, tm))
        for npos in nposs:
            q.append((npos, tm))

    return tm


FIRST_LEG = get_quickest()
print(FIRST_LEG)

SECOND_LEG = get_quickest(END, START, FIRST_LEG)
THIRD_LEG = get_quickest(START, END, SECOND_LEG)
print(THIRD_LEG)
