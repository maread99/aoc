"""Day 21: Step Counter

part b: Didn't get it out after umpteen hours.
Spent a while trying to replicate the map out from the center. First took
copies in the cardinal directions, then realised that needed to include
the diagonals, then realised that it still doesn't work as lose maps on the
next iteration. Instead, created by rows and columns then set S to the
middle of the middle one.

Believe the solve is about identifying a pattern and extrapolating
forwards. Got number of end plots for each of the first 2500 steps.
Identified a pattern in about 2hr 30 although didn't appreciate
that it was arithmetic until nearly 4hrs. Was able to get out all the
expected answers at all steps shown for the example. Realised that it was
never going to work for odd steps and changed the implementation to only
record the end plots on odd counts. Found a series in the odd steps data,
extrapolated out in the same way as for the even data (that got the
answers out for the example), but wasn't getting the correct answer for
the required number of steps. Either there's a problem in the pattern
recognition (although it was coming out for the even steps) or in the
implementation to evaluate the number of end plots for odd counts, although
I can't see it.

It's in the right ball park as submitting answers one `n` apart resulted in
a 'TOO HIGH' and a 'TOO LOW' guess.

I can't see why this doesn't work. I haven't since come across anyone that
sought to solve in the same way. Who knows why this wasn't coming out?
"""

print("THIS IMPLEMENTAION DOES NOT SOLVE!")

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

# NOTE TOGGLE LINES for example / real input
# DIM_EXPANSION = 199  # for EXAMPLE data
# for REAL data...
DIM_EXPANSION = 45  # 2 to double (4 base grids), 3 to triple (9 base grids)
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


queue = deque([(S, 0)])  # tuples of (loc, count)
# NOTE TOGGLE LINES for example / real input
STEPS = 2500  # for REAL data
# STEPS = 1000 # fpr EXAMPLE data
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

        # NOTE TOGGLE LINES for EVEN (example) / ODD (real) step
        # FOR EVEN step
        # if not (i + 1) % 2:
        #     end_plots.add(nloc)
        # FOR ODD step
        if (i + 1) % 2:
            end_plots.add(nloc)

# NOTE TOGGLE LINES for example / real data
# STEP = 5000  # for example
STEP = 26501365  # for real

# NOTE TOGGLE LINES for EVEN (example) / ODD (real) step
# end_plots_srs = end_plots_for_steps[::2]  # end plots for even steps
end_plots_srs = end_plots_for_steps[1::2]  # end plots for odd steps
diffs = [b - a for a, b in itertools.pairwise(end_plots_srs)]
i = 0
pat_lens = []
pat_valss = []
for i in range(0, STEPS // 2):
    i += 1
    diffs_diff = [b - a for a, b in itertools.pairwise(diffs[::i])]
    if len(diffs_diff) > 3 and len(set(diffs_diff[2:])) == 1:
        pat_lens.append(i)
        pat_valss.append(diffs_diff)

pat_len, pat_vals = pat_lens[0], pat_valss[0]
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
# NOTE TOGGLE LINES for EVEN (example) / ODD (real) step
len_srs = (STEP // 2) + 1  # FOR ODD step
# len_srs = (STEP // 2)  # FOR EVEN step
n, r = divmod(len_srs, pat_len)
# take off any number of pattern length before the pattern established
n -= ptrn_start_idx // pat_len
# offset to account for remainder
using_pat_intervals = [
    (a, b) for a, b in itertools.pairwise(end_plots_srs[ptrn_start_idx + r :: pat_len])
]
# initial value of arithmetic series to be summed
a = using_pat_intervals[0][1] - using_pat_intervals[0][0]

# sum of arithmetic series
ans = int((n / 2) * ((2 * a) + ((n - 1) * d))) + end_plots_srs[ptrn_start_idx + r]


print(
    "evaluates to: <",
    ans,
    "> BUT THIS IS INCORRECT - THIS IMPLEMENTATION DOES NOT SOLVE!!",
)

# TRIES
# TOO HIGH 609585292373841
# TOO LOW 609573239368795
# it's f'ing somewhere inbetween
# TOO HIGH 609591318876364 TOTAL WASTE, higher than the prior HIGH !!!
# 609585292373840 WRONG (one less than original answer)
# 609588262339984 WRONG n = 101150 (202300 / 2), r = 65
# 609585229253302 WRONG n = 101150 (202300 / 2), r = 32
# 609573282256082 WRONG n = 101149, r = 33
# 609585335261552 WRONG n, r (101150, 33)   THIS IS THE CURRENT BEST GUESS!
