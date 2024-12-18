"""Day 18: RAM Run

Alternative solution for part b. Simply iterates through each newly fallen
byte and uses the part a BFS to see if can find the end for the new
arrangement. Nothing any more fancy was requried...

(Takes <10 seconds to execute, which is slower than my actual solution
(`18.py`) although the quicker write time here would have compensated for
the slower execution 50 fold.)

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

BOUNDARY = set()
for i in range(-1, DIM + 1):
    BOUNDARY.add((-1, i))
    BOUNDARY.add((DIM, i))
    BOUNDARY.add((i, -1))
    BOUNDARY.add((i, DIM))

VECS = ((0, -1), (0, 1), (-1, 0), (1, 0))

# part a

START = (0, 0)
END = (DIM - 1, DIM - 1)

queue = deque([(START, 0)])
obs = BOUNDARY | set(BYTS[:INITIAL_FALL])
seen = set()
while queue:
    loc, n = queue.popleft()
    for v in VECS:
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

print(n)


# part b

for i, byt in enumerate(BYTS[INITIAL_FALL:]):
    queue = deque([(START, 0)])
    obs = BOUNDARY | set(BYTS[: INITIAL_FALL + i + 1])
    seen = set()
    while queue:
        break_ = False
        loc, n = queue.popleft()
        for v in VECS:
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
    else:  # if didn't break out of the while loop then will ended without reaching end
        print(byt)
        break
