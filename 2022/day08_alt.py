"""Day 8: Treetop Tree House

Written after seeing:
    https://github.com/iKevinY/advent/blob/f91e1e3ac1b6da9c1238949589ae9d09ed7e8356/2022/day08.py
Like this solution for using a dict to represent the grid and vectors to move around it.
"""

from aocd import get_data

raw = get_data(day=8, year=2022)

grid = {}
for j, row in enumerate(raw.splitlines()):
    for i, tree in enumerate(row):
        grid[i, j] = int(tree)

VECS = ((0, 1), (0, -1), (1, 0), (-1, 0))

count = 0

for loc, h in grid.items():
    prev = count
    for dx, dy in VECS:
        x, y = loc
        while True:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in grid:
                count += 1
                break
            if grid[nx, ny] >= h:
                break
            x, y = nx, ny
        if count > prev:  # tree was added in most recent direction checked
            break
print(count)


max_score = 0
for loc, h in grid.items():
    score = 1
    for dx, dy in VECS:
        count = 0
        x, y = loc
        while True:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in grid:
                break
            if grid[nx, ny] >= h:
                count += 1
                break
            count += 1
            x, y = nx, ny
        score *= count
    max_score = max(max_score, score)
print(max_score)
