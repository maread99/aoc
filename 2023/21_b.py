"""Day 21: Step Counter

part b: Umpteen hours.
Spent a while trying to replicate the map out from the center. First took
copies in the cardinal directions, then realised that needed to include
the diagonals, then realised that it still doesn't work as lose maps on the
next iteration. Instead, created by rows and columns then set S to the
middle of the middle one.

identified a pattern and extrapolated forwards. Got number of end plots
for each of the first 2500 steps. Identified the pattern in about 2hr 30
although didn't appreciate that it was arithmetic until nearly 4hrs. Was
able to get out all the expected answers at all steps shown for the
examplem, but not the answer for the actual data. Realised that it was
never going to work for odd steps and changed the implementation to
record end plots on odd counts if target step is odd. Still wasn't getting
the right answer. Couldn't see why it wasn't coming out. Only when I got
the answer by copying a different implementation (with a different
approach) was I able to then debug and realise that the remainder was 1
higher than required, or rather that the remainder had to be accounted for
by considering the series as at one index position prior to the remainder.
"""

import itertools
from collections import deque

from aocd import get_data


raw = get_data(day=21, year=2023)

# raw = """...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# """

rows = raw.splitlines()

assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

BASE_GRID = {}
for j, row in enumerate(rows):
    for i, c in enumerate(row):
        if c == "S":
            S = complex(i, j)
            c = "."
        BASE_GRID[complex(i, j)] = c


GRID = {}

# DIM_EXANSION 2 to double (4 base grids), 3 to triple (9 base grids)
DIM_EXPANSION = 29  # NOTE change to 199 for example
assert DIM_EXPANSION % 2  # maintain total number of maps as a square number
for loc, c in BASE_GRID.items():
    i, j = loc.real, loc.imag
    for i_ in range(0, DIM_EXPANSION):
        for j_ in range(0, DIM_EXPANSION):
            GRID[complex(i + DIM * i_, j + DIM * j_)] = c

num_bases = DIM_EXPANSION**2
assert len(GRID) == len(BASE_GRID) * num_bases

translation = DIM * (DIM_EXPANSION // 2)
S = complex(S.real + translation, S.imag + translation)

# Direction vectors
# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRS = (UP, DOWN, LEFT, RIGHT)


STEP = 26501365  # for real, NOTE change to 5000 for example
TARGET_STEP_ODD = bool(STEP % 2)

queue = deque([(S, 0)])  # tuples of (loc, count)
STEPS = 1500  # NOTE change to 1000 for example
seen = set()
end_plots = set()
end_plots_for_steps = [0] + ([0] * STEPS)
while queue:
    loc, i = queue.popleft()
    end_plots_for_steps[i] = max(end_plots_for_steps[i], len(end_plots))
    if i == STEPS:
        continue
    for d in DIRS:
        nloc = loc + d
        if nloc in seen:
            continue
        if GRID[nloc] == "#":
            continue
        queue.append((nloc, i + 1))
        seen.add(nloc)

        if TARGET_STEP_ODD:
            if (i + 1) % 2:
                end_plots.add(nloc)
        else:  # target step is EVEN
            if not (i + 1) % 2:
                end_plots.add(nloc)


start = 1 if TARGET_STEP_ODD else 2
end_plots_srs = end_plots_for_steps[start::2]
diffs = [b - a for a, b in itertools.pairwise(end_plots_srs)]
pat_lens = []
pat_valss = []
for i in range(1, 2000):
    diffs_diff = [b - a for a, b in itertools.pairwise(diffs[::i])]
    if len(diffs_diff) > 3 and len(set(diffs_diff[2:])) == 1:
        pat_lens.append(i)
        pat_valss.append(diffs_diff)

pat_len, pat_vals = pat_lens[-1], pat_valss[-1]
ptrn_start_idx = (
    pat_vals.index(pat_vals[-1]) * pat_len
)  # get index from where pattern asserts

diffs_over_ptn = []
for i_ in range(pat_len):
    diffs_diff_ = [
        b - a for a, b in itertools.pairwise(diffs[ptrn_start_idx + i_ :: pat_len])
    ]
    diffs_over_ptn.append(diffs_diff_[-1])

# sum of differences over pattern, i.e. value by which difference in increase in number
# of end plots over a pattern increases from one pattern to the next
d = sum(diffs_over_ptn)
len_srs = (STEP // 2) + (1 if TARGET_STEP_ODD else 0)
n, r = divmod(len_srs, pat_len)
# take off any number of pattern length before the pattern established
n -= ptrn_start_idx // pat_len
# offset to account for remainder
using_pat_intervals = [
    (a, b)
    for a, b in itertools.pairwise(end_plots_srs[ptrn_start_idx + r - 1 :: pat_len])
]
# initial value of arithmetic series to be summed
a = using_pat_intervals[0][1] - using_pat_intervals[0][0]

# sum of arithmetic series
ans = int((n / 2) * ((2 * a) + ((n - 1) * d))) + end_plots_srs[ptrn_start_idx + r - 1]
print(ans)
