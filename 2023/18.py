"""Day 18: Lavaduct Lagoon

part a: 120mins
Spent nearly 2hrs trying to work across rows going from the outside to the
inside, similar to day 10. Took a step back and asked 'why don't I just
flood the interior with a dumb BFS'. 10mins to implement.

part b: 69mins
"Well flooding it ain't gonna work". Rather than dive back into considering
inside / outside convinced myself that all that's realy going on is adding
and subtracting areas when move up and down. Answer for the example was a
bit out, on inspection saw that I could reconcile it by, instead of
adding the full boundary size, adding just half of it + 1. It worked.
`18.png` tries to explain why it's necessary to add on just half the
boundary plus 1. However, I'm not that convinced by it. I suspect a more
thorough explanation can be offered by considering this as a simple case,
applicable only to orthogonal forms, of using the shoelace method adjusted
by Picks theorm (which seems to be the common way to have solved). That
too requires adding half the perimeter + 1 to the evaluated area.

total: 189mins, 9x bottom of the leaderboard.

#BFS  #complex-numbers  #areas
"""

from collections import deque

from aocd import get_data

raw = get_data(day=18, year=2023)

# raw = """R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)
# """

LINES = raw.splitlines()

lines = []
for line_ in LINES:
    rd, rv, rc = line_.split()
    lines.append((rd, int(rv), rc[1:-1]))

# Direction vectors
# real horizontal, right positive, left negative
# j imag vertical, down positive, up negative
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
DIRS = (UP, DOWN, LEFT, RIGHT)

VEC_MAP = {
    "U": -1j,
    "D": 1j,
    "L": -1,
    "R": 1,
}

at = complex(0, 0)
BOUNDARY = set((at,))
for d, v, _ in lines:
    for i in range(v):
        at += VEC_MAP[d]
        BOUNDARY.add(at)

assert complex(1, 1) not in BOUNDARY

queue = deque([complex(1, 1)])
seen = BOUNDARY
count = len(BOUNDARY)
while queue:
    c = queue.pop()
    if c in seen:
        continue
    seen.add(c)
    count += 1
    for d in DIRS:
        nc = c + d
        if nc in seen:
            continue
        queue.appendleft(nc)

print(count)


# part b

VEC_MAP = {
    "3": UP,
    "1": DOWN,
    "2": LEFT,
    "0": RIGHT,
}

lines = []
for line_ in LINES:
    rd, rv, rc = line_.split()
    lines.append((VEC_MAP[rc[-2]], int(rc[2:-2], 16)))

area = 0
at = complex(0, 0)
for d, v in lines:
    at += d * v
    if d in (UP, DOWN):
        area += (v * int(at.real)) * (1 if d == DOWN else -1)

perimeter = sum(line[1] for line in lines)
print(area + (perimeter // 2) + 1)
