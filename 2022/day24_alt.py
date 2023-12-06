"""Day 24: Blizzard Basin.

This alternative solution only evaluates the blizzard positons in their
initial state, holding then in four sets according to their direction.
Then, for each direction, transforms each possible new position back to the
position that a blizzard would have to have started at in order to coincide
with the possible new position. If there was a blizzard there of a
direction that would cause it to conincide the proposed new position x
minutes later then can't move to that new position.

This approach requires considerably lesser code, and it's much quicker,
solving in about second rather than the 10s for the revised version.
However, it took me longer to write this, even knowing all the
background. This was in part due to a lack of experience with modulus
operations, although I get the impression the use of modulus ops requires
the data to adher to a set form, any divergences to which can cause
deugging headaches (for example the start sitting outside of the main
grid requires specific consideration. This is the reason the 'looking for
new positions' clause here differs from the referenced solution - different
ways to get around the issue).

This alternative approach was inspired by:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day24p1.py
"""

from collections import deque

from aocd import get_data


raw = get_data(day=24, year=2022)
lines = raw.splitlines()

START = (lines[0].index(".")-1, -1)
END = (lines[-1].index(".")-1, len(lines) - 2)

BS, border = [set(), set(), set(), set()], set()
BS_INDICES = "<>^v"
for j, line in enumerate(lines):
    for i, char in enumerate(line):
        # define grid based on row / col -1 as row / col on which blizzards should wrap 
        pos = (i-1, j-1)
        if char in BS_INDICES:
            BS[BS_INDICES.find(char)].add(pos)
        if char == "#":
            border.add(pos)

border.add((START[0], START[1]-1))  # add border behind entrance
border.add((END[0], END[1]+1))  # add border behond exit
LEN_ROWS = len(lines) - 2
LEN_COLS = len(lines[0]) - 2

def bfs(start=START, end=END, start_tm=0) -> int:
    q = deque([(start, start_tm)])
    seen = set()

    while q:
        pos, tm = q.popleft()
        tm += 1

        for dc, dr in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
            npos = (pos[0]+dc, pos[1]+dr)
            if npos in border:
                continue
            if npos == end:
                return tm
            
            for n, (i, d) in enumerate([(0, 1), (0, -1), (1, 1), (1, -1)]):
                bx = npos[0] if i == 1 else (npos[0] + (d * tm)) % LEN_COLS
                by = npos[1] if i == 0 else (npos[1] + (d * tm)) % LEN_ROWS
                if (bx, by) in BS[n]:
                    break
            else:
                if (state := (npos, tm)) not in seen:
                    q.append(state)
                    seen.add(state)

    return tm

FIRST_LEG = bfs()
print(FIRST_LEG)

SECOND_LEG = bfs(END, START, FIRST_LEG)
THIRD_LEG = bfs(START, END, SECOND_LEG)
print(THIRD_LEG)
