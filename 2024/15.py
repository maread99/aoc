"""Day 15: Warehouse Woes

part a: 58mins
Unbelievably stupid bug - I wrote the UP and DOWN vectors around the wrong
way! Even worse, I didn't think to check it before launching into debugging
by printing off grids. Even worse, I spent ages over a silly bug in
defining the grid where I'd copied the first row of a blank grid to all rows
rather than having each row represented with a separate list. If not for
all that I reckon I'd have had it out in less than half hour, possibly well
under. Annoying.

part b: 1 hour 52 minutes
My big error was trying to use a bfs to identify all the boxes being
moved... doing so results in including adjacent boxes that wouldn't move.
If I'd discerened in the first place the different behaviour between
pushing left or right and pushing up or down I wouldn't have gone there. As
it was I initially made a right pigs ear out of it by completely
overcomplicating it (I effectively treated it as if the boxes were 2 x 2).

total: 2hrs 50mins, 5.3x bottom of the leaderboard.

I was pretty happy with how I codified the rules in the end.

#codify-rules. Also using #complex-numbers to navigate a #grid
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
    boxes = [{nat, nat + LEFT if bc == "]" else nat + RIGHT}]
    while True:
        move = True
        if any(grid[loc + d] == "#" for loc in boxes[-1]):
            move = False
            break
        if all(grid[loc + d] == "." for loc in boxes[-1]):
            break
        nlocs = [loc + d for loc in boxes[-1]]
        nboxes = set()
        for nloc in nlocs:
            if (c := grid[nloc]) in BOX:
                nboxes.add(nloc)
                nboxes.add(nloc + LEFT if c == "]" else nloc + RIGHT)
        boxes.append(nboxes)

    if not move:
        continue

    # advance boxes
    b_locs = set()
    for boxes_on_level in boxes:
        b_locs |= boxes_on_level

    loc_cs = [(loc, grid[loc]) for loc in b_locs]
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


# What a waste of time...

# boxes = set()
# seen = set()
# queue = deque([nat])
# while queue:
#     loc = queue.pop()
#     for ds in DIRS_SIMP:
#         nloc = loc + ds
#         if nloc in seen:
#             continue
#         seen.add(nloc)
#         if (b_ := grid.get(nloc, "X")) in BOX:
#             boxes.add((nloc, b_))
#             queue.appendleft(nloc)

# # find the front
# f = min if d in (UP, LEFT) else max
# cmp = "imag" if d in (UP, DOWN) else "real"
# f_idx = f([getattr(b[0], cmp) for b in boxes])
# # find width of advance
# cmp = "imag" if cmp == "real" else "real"
# w_idxs = [getattr(b[0], cmp) for b in boxes]
# # w = max(idxs) - min(idxs) + 1

# # look ahead of front to see if boxes can be moved
# move = True
# nidx = f_idx + (1 if d in (RIGHT, DOWN) else -1)
# for wi in range(int(min(w_idxs)), int(max(w_idxs)) + 1):
#     loc = complex(
#         wi if d in (LEFT, RIGHT) else nidx,
#         nidx if d in (UP, DOWN) else wi,
#     )
#     if grid[complex(loc)] == "#":
#         move = False
#         break
# if not move:
#     continue

# # move all the boxes forward
# for b in boxes:
#     grid[b[0]] = "."
# for b in boxes:
#     grid[b[0] + d] = b[1]
# grid[at] = "."
# grid[nat] = "@"
# at = nat
