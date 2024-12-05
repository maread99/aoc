"""Day 5: Print Queue

part a: 36mins
I overcomplicated the function to check if an update is valid (the original
version I used for the solve is commented out at the end of this file).

part b: 15mins
Quicker way to solve would have been comparative sorting (I'll put up an
alternative solve).

total: 51mins, 13.7x bottom of the leaderboard.

#lists
"""

from collections import defaultdict

from aocd import get_data

raw = get_data(day=5, year=2024)

# raw = """47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47
# """

protocols_, updates_ = raw.split("\n\n")

protocols = [list(map(int, l.split("|"))) for l in protocols_.splitlines()]
updates = [list(map(int, u.split(","))) for u in updates_.splitlines()]

mp = defaultdict(list)  # map each page to pages the page much fall before
for a, b in protocols:
    mp[a].append(b)


def is_valid(update: list[int]) -> bool:
    for i, page in enumerate(update):
        for v in update[i + 1 :]:
            if page in mp[v]:  # page falls after a page that it should have come before
                return False
    return True


valid_lines: list[int] = []
invalid_lines: list[int] = []

for update in updates:
    lst = valid_lines if is_valid(update) else invalid_lines
    lst.append(update)

print(sum(l[len(l) // 2] for l in valid_lines))


crctd_updates = []
for pages in invalid_lines:
    crctd = [pages[0]]
    for page in pages[1:]:
        inserted = False
        for i, v in enumerate(crctd):
            if v in mp[page]:
                crctd.insert(i, page)
                inserted = True
                break
        if not inserted:
            crctd.append(page)
    crctd_updates.append(crctd)

print(sum(l[len(l) // 2] for l in crctd_updates))


# Overcomplicated original version of `is_valid`` used to solve:
# def is_valid(update: list[int]) -> bool:
#     rvrsd = list(reversed(update))
#     remaining_vals = [rvrsd[0]]
#     for page in rvrsd[1:]:
#         for v in remaining_vals:
#             comes_before_pages = mp[v]
#             if page in comes_before_pages:
#                 return False
#         remaining_vals.append(page)
#     return True
