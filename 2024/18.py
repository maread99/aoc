"""Day 18: RAM Run

NOTE: The `18_alt.py` solution's better.

part a: 51mins
Careless bug where I left a hard-coded 12 from the example! Ended up
printing out a representation of the path before I realised it. Should have
taken a THOROUGH LOOK through the code before plunging to such depths.
Then made a mess of the BFS by appending to the left of the queue rather
than the end 😳. (Before spotting the error I solved with an overkill
priority queue, although the solution here shows a BFS.)

part b: 1hours 17mins
Didn't occur to me to just repeat part a for each newly fallen byte! I
wrongly assumed such an approach would take too long to execute! Should
have thought about it a bit more! I don't learn. (See `18_alt.py` which
takes < 10 secs to run and would have been much quicker to write!)

What did occur to me was to look for the first byte that results in a
continuous barrier existing from the south edge to either the north or east
edge (thereby cutting off the path from NW to SE).

(I actually solved part b with a far more inefficient implementation than
whats's here - from every new byte I tried to reach the south edge and
either the north or west edge. Took maybe 5 minutes.)

total: 2hours 8mins, 21.7x bottom of the leaderboard.

#BFS  #sets
"""

from collections import deque

from aocd import get_data


raw = get_data(day=18, year=2024)
DIM = 71
INITIAL_FALL = 1024

# raw = """5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0
# """
# DIM = 7
# INITIAL_FALL = 12


BYTS = list((tuple(map(int, l.split(",")))) for l in raw.splitlines())
EMPTY = {(i, j) for i in range(DIM) for j in range(DIM)}
EMPTY -= set(BYTS[:INITIAL_FALL])

BOUNDARY = set()
for i in range(-1, DIM + 1):
    BOUNDARY.add((-1, i))
    BOUNDARY.add((DIM, i))
    BOUNDARY.add((i, -1))
    BOUNDARY.add((i, DIM))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UP_L = (-1, -1)
UP_R = (1, -1)
DOWN_L = (-1, 1)
DOWN_R = (1, 1)

VECS4 = (UP, DOWN, LEFT, RIGHT)
VECS8 = (UP, DOWN, LEFT, RIGHT, UP_L, UP_R, DOWN_L, DOWN_R)

# part a

START = (0, 0)
END = (DIM - 1, DIM - 1)

queue = deque([(START, 0)])
obs = BOUNDARY | set(BYTS[:INITIAL_FALL])
seen = set()
break_ = False
while queue:
    loc, n = queue.popleft()
    for v in VECS4:
        nloc = (loc[0] + v[0], loc[1] + v[1])
        if nloc in obs:
            continue
        if nloc in seen:
            continue
        if nloc == END:
            n += 1
            break_ = True
            break
        seen.add(nloc)
        queue.append((nloc, n + 1))
    if break_:
        break
print(n)


# part b

barriers = set()


def extend_barriers(byt):
    if byt[0] == DIM - 1 or byt[1] == 0:  # new byt itself extends barrier to an edge
        print(byt)
        exit()
    barriers.add(byt)
    nogo = BOUNDARY | EMPTY
    queue = [byt]
    while queue:
        loc = queue.pop()
        for v in VECS8:
            nloc = (loc[0] + v[0], loc[1] + v[1])
            if nloc in barriers | nogo:
                continue
            if nloc[0] == DIM - 1 or nloc[1] == 0:  # get to East or North edge
                print(byt)
                exit()
            barriers.add(nloc)
            queue.append(nloc)


# define barriers from south wall
barrier_starts = [byt for byt in BYTS[:INITIAL_FALL] if byt[1] == DIM - 1]
for start in barrier_starts:
    extend_barriers(start)

for it, byt in enumerate(BYTS[INITIAL_FALL:]):
    EMPTY.remove(byt)
    for v in VECS8:
        if byt[1] == DIM - 1 or (byt[0] + v[0], byt[1] + v[1]) in barriers:
            extend_barriers(byt)
            break
