"""Day 10: Pipe Maze

NOTE: NOT A GENERAL SOLUTION. Requires identifying and hard-coding the
symbol corresponding with S.

part a: 33mins

part b: 2hrs 45mins
First considered a search to find everything that's clearly outside and
then explore each of the pockets to see if there was a way out, potentially
using 0.5 in the real and imag parts of the complex number to simulate
moving between neighbouring pipes.

Before diving in considered if a better way wouldn't be to explore whether
could switch between inside and outside as move across a row (or down a
column). Nearly abandoned the idea when it wasn't coming out although
convinced myself that the principle should hold and got to the crux of
it - you only move from inside to outside when you actually CROSS a pipe.

total: 3hrs 18mins, 5.4 bottom of the leaderboard.

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

S_SYMB = "7"  # NOTE: BY INSPECTION   # S can go down or left, it's a 7
# S_SYMB = "F"  # For exmaple

GRID = {}
rows = raw.splitlines()
for r, row in enumerate(rows):
    for c, symb in enumerate(row):
        if symb == "S":
            S = complex(c, r)
            symb = S_SYMB
        GRID[complex(c, r)] = symb

# part a

# positive down and right, negative up and left
VECS = {
    "|": (-1j, 1j),
    "7": (1j, -1),
    "F": (1j, 1),
    "-": (1, -1),
    "L": (-1j, 1),
    "J": (-1j, -1),
}

pat = S
at = pat + VECS[S_SYMB][1]
pipe_path = {pat, at}
count = 1
while True:
    pipe = GRID[at]
    vecs = VECS[pipe]
    nat = at + vecs[0] if at + vecs[0] != pat else at + vecs[1]
    pat = at
    at = nat
    pipe_path.add(at)
    count += 1
    if at == S:
        break

print(count // 2)

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
            if symb == "|":
                outside = not outside
            elif symb in ("L", "F"):
                entered = symb
            elif symb in ("J", "7"):
                assert entered, t
                if (entered == "L" and symb == "7") or (entered == "F" and symb == "J"):
                    # crossed pipe
                    outside = not outside
                entered = ""
        elif not outside:
            count += 1

print(count)
