"""Day 4: Ceres Search

part a: 25mins
part b: 19mins

total: 44mins, 7.7x bottom of the leaderboard.

#grid #complex-numbers
"""

from aocd import get_data

raw = get_data(day=4, year=2024)

# raw = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# """

rows = raw.splitlines()

GRID = {}
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        GRID[complex(i, j)] = c

VECS = (
    -1j,  # up
    1 - 1j,  # up right
    1,  # right
    1 + 1j,  # down right
    1j,  # down
    -1 + 1j,  # down left
    -1,  # left
    -1 - 1j,  # up left
)

total = 0
for loc, v in GRID.items():
    if v != "X":
        continue
    for vec in VECS:
        if GRID.get(loc + vec, False) != "M":
            continue
        if GRID.get(loc + (vec * 2), False) != "A":
            continue
        if GRID.get(loc + (vec * 3), False) != "S":
            continue
        total += 1
print(total)


UP_L = -1 - 1j
UP_R = 1 - 1j
DOWN_L = -1 + 1j
DOWN_R = 1 + 1j

ENDS = ("M", "S")
total = 0
for loc, v in GRID.items():
    if v != "A":
        continue
    if (up_l := GRID.get(loc + UP_L, False)) not in ENDS:
        continue
    if (down_r := GRID.get(loc + DOWN_R, False)) not in ENDS:
        continue
    if up_l == down_r:
        continue

    if (up_r := GRID.get(loc + UP_R, False)) not in ENDS:
        continue
    if (down_l := GRID.get(loc + DOWN_L, False)) not in ENDS:
        continue
    if up_r == down_l:
        continue

    total += 1
print(total)
