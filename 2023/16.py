"""Day 16: The Floor Will Be Lava

part a: 75mins
Took a while to debug that I hadn't SET THE INPUT TO A RAW STRING and hence
was escaping a '/' in '//'!

part b: 21mins
Misread the question, thinking that required the total number of tiles that
would be energised if a ray entered at each edge tile, rather than the max
that could be energised with a single ray entering at any edge tile - READ
THE QUESTION!

total: 96mins. 6.2x bottom of the leaderboard.

NB part 1 and part 2 times on personal leaderboard are miles apart as had
to dash out and finish it later.

#grid #complex-numbers #vectors
"""

from aocd import get_data


raw_ = get_data(day=16, year=2023)
raw = rf"{raw_}"

# raw = r""".|...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\
# ..../.\\..
# .-.-/..|..
# .|....-|.\
# ..//.|....
# """

rows = raw.splitlines()

MIRRORS = {}

for j, row in enumerate(rows):
    for i, c in enumerate(row):
        loc = complex(i, j)
        if c != ".":
            MIRRORS[loc] = c

assert len(rows) == len(rows[0]), (len(rows), len(rows[0]), rows)  # assert square
DIM = len(rows)

BOUNDARY = set()
for i in range(-1, DIM + 1):
    BOUNDARY.add(complex(-1, i))
    BOUNDARY.add(complex(DIM, i))
    BOUNDARY.add(complex(i, -1))
    BOUNDARY.add(complex(i, DIM))


# Direction vectors
# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1

CHG_DIR = {
    ("/", UP): RIGHT,
    ("/", DOWN): LEFT,
    ("/", LEFT): DOWN,
    ("/", RIGHT): UP,
    ("\\", UP): LEFT,
    ("\\", DOWN): RIGHT,
    ("\\", LEFT): UP,
    ("\\", RIGHT): DOWN,
}

REFLECTORS = ("/", "\\")


def shoot_ray(loc_: complex, facing_: complex):
    seen = set()

    def shoot(loc: complex, facing: complex):
        while True:
            if (loc, facing) in seen:
                break
            seen.add((loc, facing))
            loc += facing
            if loc in BOUNDARY:
                break
            if m := MIRRORS.get(loc, False):
                if m in REFLECTORS:
                    facing = CHG_DIR[(m, facing)]
                    continue

                if m == "|":
                    if facing in (UP, DOWN):
                        continue
                    shoot(loc, UP)
                    facing = DOWN
                else:
                    # assert m == "-"
                    if facing in (LEFT, RIGHT):
                        continue
                    shoot(loc, LEFT)
                    facing = RIGHT

    shoot(loc_, facing_)
    been = {s[0] for s in seen}
    return len(been) - 1  # -1 to remove boundary tile that started from


# part a

print(shoot_ray(complex(-1, 0), RIGHT))

# part b

max_ = 0
for t in BOUNDARY:
    if t.imag == t.real:
        continue  # corners
    elif t.real == -1:
        facing = RIGHT
    elif t.imag == -1:
        facing = DOWN
    elif t.real == DIM:
        facing = LEFT
    else:
        facing = UP
    max_ = max(max_, shoot_ray(t, facing))

print(max_)
