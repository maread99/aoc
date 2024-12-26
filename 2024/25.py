"""Day 25: Code Chronicle

part a: 30mins
Couple of silly bugs from rushing it.

total: 30mins, 6.6x bottom of the leaderboard.
"""

from aocd import get_data

raw = get_data(day=25, year=2024)

# raw = """#####
# .####
# .####
# .####
# .#.#.
# .#...
# .....

# #####
# ##.##
# .#.##
# ...##
# ...#.
# ...#.
# .....

# .....
# #....
# #....
# #...#
# #.#.#
# #.###
# #####

# .....
# .....
# #.#..
# ###..
# ###.#
# ###.#
# #####

# .....
# .....
# .....
# #....
# #.#..
# #.#.#
# #####
# """

blocks = raw.split("\n\n")

LOCKS = []
KEYS = []
for block in blocks:
    if set(block.splitlines()[0]) == {"#"}:
        LOCKS.append(block)
    else:
        KEYS.append(block)

locks = []
for lock in LOCKS:
    locks.append(tuple(c.count("#") for c in zip(*lock.splitlines())))

keys = []
for key in KEYS:
    keys.append(tuple(c.count("#") for c in zip(*key.splitlines())))

num = 0
for lock in locks:
    for key in keys:
        if all(b <= (7 - a) for a, b in zip(lock, key)):
            num += 1
print(num)
