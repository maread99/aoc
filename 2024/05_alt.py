"""Day 5: Print Queue

Solves part b using comparative sorting.

#lists  #sort  #compare
"""

from collections import defaultdict
import functools

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


valid_updates: list[int] = []
invalid_updates: list[int] = []

for update in updates:
    lst = valid_updates if is_valid(update) else invalid_updates
    lst.append(update)

print(sum(l[len(l) // 2] for l in valid_updates))


key = functools.cmp_to_key(lambda a, b: -1 if b in mp[a] else 1)
crctd_updates = [sorted(iu, key=key) for iu in invalid_updates]
print(sum(l[len(l) // 2] for l in crctd_updates))
