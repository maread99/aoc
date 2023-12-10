"""Day 10: Pipe Maze

Offers a general solution by evaluating symbol at S.

Also simplifies part a.

#complex-numbers #grid
"""

from aocd import get_data

raw = get_data(day=10, year=2023)

# raw = """7-F7-
# .FJ|7
# SJLL7
# |F--J
# LJ.LJ
# """

# raw = """...........
# .S-------7.
# .|F-----7|.
# .||OOOOO||.
# .||OOOOO||.
# .|L-7OF-J|.
# .|II|O|II|.
# .L--JOL--J.
# .....O.....
# """

# raw = """FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L
# """

GRID = {}
rows = raw.splitlines()
for r, row in enumerate(rows):
    for c, symb in enumerate(row):
        if symb == "S":
            S = complex(c, r)
        GRID[complex(c, r)] = symb

# positive down and right, negative up and left
VECS = {
    "|": (-1j, 1j),
    "7": (1j, -1),
    "F": (1j, 1),
    "-": (1, -1),
    "L": (-1j, 1),
    "J": (-1j, -1),
}

# Identify symbol for S.
# Included to make solution general, although quicker to manually identify
# and hard-code, for example, `GRID[S] = "|"`
for symb, (a_, b_) in VECS.items():
    a, b = S + a_, S + b_
    a_symb, b_symb = GRID.get(a, "."), GRID.get(b, ".")
    if a_symb == "." or b_symb == ".":
        continue
    if (a + VECS[a_symb][0]) != S and (a + VECS[a_symb][1]) != S:
        continue
    if (b + VECS[b_symb][0]) != S and (b + VECS[b_symb][1]) != S:
        continue
    GRID[S] = symb
    break
else:
    assert False, "didn't match symb"


# part a

at = S
pipe_path = {at}
while True:
    t = GRID[at]
    vecs = VECS[t]
    nat = at + vecs[0]
    if nat in pipe_path:
        nat = at + vecs[1]
    at = nat
    pipe_path.add(at)
    if at == S:
        break

print(len(pipe_path) // 2)

# part b

# work across each row
count = 0
for r, row in enumerate(rows):
    outside = True
    entered = ""
    for c in range(len(row)):
        t = complex(c, r)
        if t in pipe_path:
            symb = GRID[t]
            if symb == "|":  # crossing pipe
                outside = not outside
            elif symb in ("L", "F"):
                entered = symb
            elif symb in ("J", "7"):
                if (entered == "L" and symb == "7") or (entered == "F" and symb == "J"):
                    # crossed pipe
                    outside = not outside
                entered = ""
        elif not outside:
            count += 1

print(count)
