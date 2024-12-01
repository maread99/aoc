"""Day 1: Historian Hysteria

part a: 13mins
part b: 4mins

Rusty, couldn't think how to reverse zip, and not having set the new
session cookie for aocd didn't help.

total: 17mins, 6.7x bottom of the leaderboard.

#lists #sort #zip
"""

from aocd import get_data


raw = get_data(day=1, year=2024)

# raw = """3   4
# 4   3
# 2   5
# 1   3
# 3   9
# 3   3
# """

lines = [tuple(map(int, l.split("   "))) for l in raw.splitlines()]

list_a, list_b = zip(*lines)

print(sum(abs(a - b) for a, b in zip(sorted(list_a), sorted(list_b))))

print(sum(a * list_b.count(a) for a in list_a))
