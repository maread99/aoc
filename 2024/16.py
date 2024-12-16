"""Day 16: Reindeer Maze

part a: 38mins
I was happy to get a part a out this quickly on a puzzle that would have
taken me forever a couple of years back. Then...

part b: 4hrs 22mins
Took me an age.

Solved on a similar basis to part a although:
    includes to the state the path taken

    for every (location, direction) that comes off the queue it looks to
    see if the current score ADDED to the cheapest path from that
    (location, direction) to the E equals the (now known) minimum cost,
    i.e does the (location, direction) lie on a best path. If so, the
    current path is added to a global set. This way all locations of all
    the best paths find their way into that global set (except the E, hence
    the plus one at the end).

Executes in about 7secs on my machine. I suspect there's a far neating way
of doing this, maybe on a more recursive basis. (I'll write up a revision
or alternative version if I get a chance.)

total: 4hrs 59mins, 21.7x bottom of the leaderboard.

#Dijkstra
"""

import functools
import heapq
import math

from aocd import get_data

raw = get_data(day=16, year=2024)

# raw = """###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############
# """

# raw = """#################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#^#
# #.#.#.#...#...#^#
# #.#.#.#.###.#.#^#
# #>>v#.#.#.....#^#
# #^#v#.#.#.#####^#
# #^#v..#.#.#>>>>^#
# #^#v#####.#^###.#
# #^#v#..>>>>^#...#
# #^#v###^#####.###
# #^#v#>>^#.....#.#
# #^#v#^#####.###.#
# #^#v#^........#.#
# #^#v#^#########.#
# #S#>>^..........#
# #################
# """

rows = raw.splitlines()

grid = {}
for j, r in enumerate(rows):
    for i, c in enumerate(r):
        grid[(i, j)] = c
        if c == "S":
            START = (i, j)
        if c == "E":
            END = (i, j)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
VECS = (UP, DOWN, LEFT, RIGHT)


@functools.cache
def get_minscore(start, d):
    queue = [(0, start, d)]
    heapq.heapify(queue)
    seen = {start}
    min_scr = math.inf
    while queue:
        scr, loc, d = heapq.heappop(queue)
        if scr > min_scr:
            return min_scr
        for vec in VECS:
            nloc = loc[0] + vec[0], loc[1] + vec[1]
            if grid[nloc] == "#":
                continue
            nscr = scr + (1 if d == vec else 1001)

            if nloc in seen:
                continue
            seen.add(nloc)

            if nloc == END:
                if nscr < min_scr:
                    min_scr = nscr

            heapq.heappush(queue, (nscr, nloc, vec))
    return math.inf


# part a

MIN_SCORE = get_minscore(START, RIGHT)
print(MIN_SCORE)

# part b

queue = [(0, START, RIGHT, (START,))]  # state as score, loc, direction, path taken
heapq.heapify(queue)
seen = {START}
tiles = set()
while queue:
    scr, loc, d, path = heapq.heappop(queue)
    if scr > MIN_SCORE:
        break
    for vec in VECS:
        nloc = loc[0] + vec[0], loc[1] + vec[1]
        if grid[nloc] == "#":
            continue
        nscr = scr + (1 if d == vec else 1001)
        npath = path + (nloc,)

        if nscr + get_minscore(nloc, vec) == MIN_SCORE:
            tiles |= set(npath)
        else:
            continue

        heapq.heappush(queue, (nscr, nloc, vec, npath))

print(len(tiles) + 1)
