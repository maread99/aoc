"""Day 11: Cosmic Expansion

part a: 24mins
Originally did by actually expanding the rows and columns (commented out
at bottom of file). Rewrote the implementation during part b to provide for
defining large expansion values.

part b: 58mins
Terrible. Took an age to find a stupid bug confusing columns and rows in
the expansion part of the `shortest_path` function. Should have spotted it
way earlier by inspection of the code, instead ended up tracking it down by
comparing the result of my original part a implemenation with that of the
revised implementation.

Didn't actually take too long to realise the need to drop the expansion
value by 1.

total: 82mins, 8.5x bottom of the leaderboard.

#sets #grid #arrays #manhattan
"""

from aocd import get_data

raw = get_data(day=11, year=2023)

# raw = """...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....
# """

rows = []
cols = []
ROWS_EXPANSION = []
COLS_EXPANSION = []

for row in raw.splitlines():
    rows.append(row)
    exp = 1 if len(set(row)) == 1 and row[0] == "." else 0
    ROWS_EXPANSION.append(exp)

for [*col_] in zip(*rows):
    col = "".join(col_)
    cols.append(col)
    exp = 1 if len(set(col)) == 1 and col[0] == "." else 0
    COLS_EXPANSION.append(exp)

GALAXIES = set()

for r, row in enumerate(rows):
    for c, symb in enumerate(row):
        if symb == "#":
            GALAXIES.add((c, r))


def shortest_distance(a: tuple[int, int], b: tuple[int, int], exp_rate: int) -> int:
    if a == b:
        return 0
    ax, ay = a
    bx, by = b
    # careless bug, confusing rows and cols!
    # num_expanded_rows = sum(ROWS_EXPANSION[min(ax, bx): max(ax, bx)])
    # num_expanded_cols = sum(COLS_EXPANSION[min(ay, by): max(ay, by)])
    # dist_x = abs(bx - ax) + (num_expanded_rows * exp_rate)
    # dist_y = abs(by - ay) + (num_expanded_cols * exp_rate)
    # corrected
    num_expanded_rows = sum(ROWS_EXPANSION[min(ay, by) : max(ay, by)])
    num_expanded_cols = sum(COLS_EXPANSION[min(ax, bx) : max(ax, bx)])
    dist_x = abs(bx - ax) + (num_expanded_cols * exp_rate)
    dist_y = abs(by - ay) + (num_expanded_rows * exp_rate)
    return dist_x + dist_y


def shortest_distances(
    a: tuple[int, int], others: set[tuple[int, int]], exp_rate: int
) -> list[int]:
    dists = []
    for b in others:
        dists.append(shortest_distance(a, b, exp_rate))
    return dists


total = 0
for galaxy in GALAXIES:
    total += sum(shortest_distances(galaxy, GALAXIES, 1))
print(total // 2)

total = 0
for galaxy in GALAXIES:
    total += sum(shortest_distances(galaxy, GALAXIES, 999_999))
print(total // 2)


# original part a implementation

# rows_ = []
# cols = []

# # expand

# for row in raw.splitlines():
#     rows_.append(row)
#     if len(set(row)) == 1 and row[0] == ".":
#         rows_.append("." * len(row))

# for [*col_] in zip(*rows_):

#     col = "".join(col_)
#     cols.append(col)
#     if len(set(col)) == 1 and col[0] == ".":
#         cols.append("." * len(col))

# rows = []

# for [*row_] in zip(*cols):
#     row = "".join(row_)
#     rows.append(row)

# GALAXIES = set()

# for r, row in enumerate(rows):
#     for c, symb in enumerate(row):
#         if symb == "#":
#             GALAXIES.add((c, r))

# def shortest_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
#     if a == b:
#         return 0
#     ax, ay = a
#     bx, by = b
#     dist = abs(bx - ax) + abs(by - ay)
#     return dist

# def shortest_distances(a: tuple[int, int], others: set[tuple[int, int]]) -> list[int]:
#     dists = []
#     for b in others:
#         dists.append(shortest_distance(a, b))
#     return dists

# total = 0
# for galaxy in GALAXIES:
#     total += sum(shortest_distances(galaxy, GALAXIES))

# print(total // 2)
