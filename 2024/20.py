"""Day 20: Race Condition

Executes in <15secs.

part a: 29mins
part b: 39mins
Annoying, I had the right solution earlier although was reading the example
answers wrongly (not considering the cumulative effect), i.e. I probably
solved part b in under half an hour but didn't bother running it on my
actual input!
ACTUALLY, overall I was lucky... afterwards I found a bug that was
preventing me getting out some of the example answers altough which didn't
seem to affect the answer for my actual input! (I'd omitted to include the
START to the distances map).

total: 68mins, 4.3x bottom of the leaderboard.

NOTE: This solution ASSUMES that all cheats take you back on to the same
unique path rather that on to a different, shorter path. I didn't look to
verify this although I suspect every "." is on the unique path.

#BFS  #sets  #manhattan
"""

from collections import deque
import itertools

from aocd import get_data

raw = get_data(day=20, year=2024)
MIN_SAVING = 100

# raw = """###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# """
# MIN_SAVING = 64  # part a ans = 1, part b ans = 86  (19 + 12 + 14 + 12 + 22 + 4 + 3)


rows = raw.splitlines()

for i, j in itertools.product(range(len(rows)), repeat=2):
    if rows[j][i] == "S":
        START = (i, j)
        break

queue = deque([(START, 0)])
dists = {START: 0}
while queue:
    loc, n = queue.popleft()
    for vec in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        nloc = loc[0] + vec[0], loc[1] + vec[1]
        if nloc in dists:
            continue
        if rows[nloc[1]][nloc[0]] == "#":
            continue
        dists[nloc] = n + 1
        queue.append((nloc, n + 1))
        if rows[nloc[1]][nloc[0]] == "E":
            break
    else:
        continue
    break

# part a
n = 0
for loc, d_loc in dists.items():
    for vec in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        nloc = loc[0] + vec[0] * 2, loc[1] + vec[1] * 2
        if d := dists.get(nloc, False):
            saving = d - d_loc - 2
            if saving >= MIN_SAVING:
                n += 1
print(n)

# part b


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


cheats = set()
for sloc, eloc in itertools.combinations(dists.keys(), r=2):
    sd = dists[sloc]
    ed = dists[eloc]
    if (md := manhattan(sloc, eloc)) <= 20:
        saving = ed - sd - md
        if saving >= MIN_SAVING:
            cheats.add((sloc, eloc))
print(len(cheats))
