"""Day 12: Hill Climbing Algorithm.

95mins part a (lot of debugging), 11mins part b
"""

from aocd import get_data

raw = get_data(day=12, year=2022)
data = raw.splitlines()
# create heightmap
grid = {}
for j, row in enumerate(data):
    for i, h in enumerate(row):
        if h == "S":
            S = (i, j)
            grid[i, j] = ord("a")
        elif h == "E":
            E = (i, j)
            grid[i, j] = ord("z")
        else:
            grid[i, j] = ord(h)

VECS = ((0, 1), (0, -1), (1, 0), (-1, 0))

shortest = float("inf")
Cell = tuple[int, int]  # coord
seen: dict[Cell, int] = {}  # key coord, value of least steps to reach
unfinished: list[tuple[Cell, int]] = [(S, 0)]  # [0] coord, [1] steps to coord

while unfinished:
    frm, count = unfinished.pop()
    count += 1
    h = grid[frm]
    for vec in VECS:
        new = frm[0] + vec[0], frm[1] + vec[1]
        if new not in grid:
            continue
        if grid[new] <= h + 1:
            if new == E:
                if count < shortest:
                    shortest = count
                continue
            prev = seen.get(new, float("inf"))
            if count < prev:
                seen[new] = count
                unfinished.append((new, count))

print(shortest)

# part b, run for each starting coord but maintaining seen outside of the
# loop to abort iterations as soon as evident that not shorter.

shortest = float("inf")
seen = {}

for S, h in grid.items():
    if chr(h) != "a":
        continue
    unfinished = [(S, 0)]
    while unfinished:
        frm, count = unfinished.pop()
        count += 1
        h = grid[frm]
        for vec in VECS:
            new = frm[0] + vec[0], frm[1] + vec[1]
            if new not in grid:
                continue
            if grid[new] <= h + 1:
                if new == E:
                    if count < shortest:
                        shortest = count
                    continue
                prev = seen.get(new, float("inf"))
                if count < prev:
                    seen[new] = count
                    unfinished.append((new, count))
print(shortest)
