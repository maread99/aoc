"""Day 15: Warehouse Woes

Tides the code for part b that identified boxes to be moved.

Inspired by hyperneutrino's solution:
    https://github.com/hyperneutrino/advent-of-code/blob/main/2024/day15p2.py

#codify-rules. Also manipulating #arrays and using #complex-numbers to
navigate a #grid
"""

from aocd import get_data

raw = get_data(day=15, year=2024)

# raw = """##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########

# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
# """

UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1

DIRS = {
    "v": DOWN,
    "^": UP,
    "<": LEFT,
    ">": RIGHT,
}

block, instr_ = raw.split("\n\n")
instr = [DIRS[c] for c in instr_ if c in DIRS]

# part a

rows = block.splitlines()

grid = {}
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        grid[complex(i, j)] = c
        if c == "@":
            at = complex(i, j)

for d in instr:
    nat = at + d
    if grid[nat] == "#":
        continue
    if grid[nat] == ".":
        grid[at] = "."
        grid[nat] = "@"
        at = nat
        continue

    loc = nat
    while grid[loc] == "O":
        loc += d
    if grid[loc] == "#":
        continue  # can't move boxes as there's a wall after them
    grid[loc] = "O"
    grid[at] = "."
    grid[nat] = "@"
    at = nat

tot = 0
for loc, c in grid.items():
    if c == "O":
        tot += (100 * loc.imag) + loc.real
print(int(tot))

# grid print
# grid_ = [["."] * len(rows[0]) for _ in range(len(rows))]
# for loc, c in grid.items():
#     grid_[int(loc.imag)][int(loc.real)] = c
# print("\n".join(["".join(l) for l in grid_]), "\n")


block = block.replace("#", "##")
block = block.replace("O", "[]")
block = block.replace(".", "..")
block = block.replace("@", "@.")
rows = block.splitlines()

BOX = ("[", "]")

grid = {}
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        grid[complex(i, j)] = c
        if c == "@":
            at = complex(i, j)

for d in instr:
    nat = at + d
    if grid[nat] == "#":
        continue
    if grid[nat] == ".":
        grid[at] = "."
        grid[nat] = "@"
        at = nat
        continue

    if d in (LEFT, RIGHT):
        loc = nat
        while grid[loc] in BOX:
            loc += d
        if grid[loc] == "#":
            continue  # can't move boxes as there's a wall after them

        loc = nat
        while (c := grid[loc]) in BOX:
            grid[loc] = "[" if c == "]" else "]"
            loc += d
        grid[loc] = "[" if d == LEFT else "]"

        grid[at] = "."
        grid[nat] = "@"
        at = nat
        continue

    bc = grid[nat]  # box character
    boxes = [nat, nat + LEFT if bc == "]" else nat + RIGHT]
    move = True
    # This loop takes advatage of python's for loops returning the nth item
    # of the list as defined at the time of the nth iteration (NOT as the
    # list was defined at the time of the first iteration). (Python
    # basically operates the actual list, not a copy.
    for loc in boxes:
        nloc = loc + d
        if grid[nloc] == "#":
            move = False
            break
        if (bc := grid[nloc]) in BOX:
            boxes.extend([nloc, nloc + LEFT if bc == "]" else nloc + RIGHT])

    if not move:
        continue

    loc_cs = [(loc, grid[loc]) for loc in boxes]
    for loc, c in loc_cs:
        grid[loc] = "."
    for loc, c in loc_cs:
        grid[loc + d] = c

    grid[at] = "."
    grid[nat] = "@"
    at = nat

tot = 0
for loc, c in grid.items():
    if c == "[":
        tot += (100 * loc.imag) + loc.real
print(int(tot))
