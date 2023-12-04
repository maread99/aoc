"""Day 4: Scratchcards

part a: 13mins
part b: 19mins
total: 32mins, 4.5x bottom of the leaderboard
"""

import re
from collections import defaultdict
from functools import reduce

from aocd import get_data


def positive_ints(s: str) -> list[int]:
    # reduced version of helpers.utils.positive_ints
    return list(map(int, re.findall(r"\d+", s)))


raw = get_data(day=4, year=2023)

lines = raw.splitlines()

# part a
# (extracts `num_wins` for part b)

num_wins = defaultdict(int)
total = 0
for i, card in enumerate(lines):
    nums_, winning_nums_ = card.split(":")[1].strip().split("|")
    # OR simpler here, just split and map to int, `nums = set(map(int, nums_.split()))`
    nums = set(positive_ints(nums_))
    winning_nums = set(positive_ints(winning_nums_))
    wins = len(nums & winning_nums)
    num_wins[i] = wins  # can 0-index as game number is not important
    if wins:
        # OR better, total += 2 ** (wins - 1)
        total += reduce(lambda a, _: a * 2, range(1, wins + 1))

print(total)

# part b

NUM_WINS = num_wins

num_cards: dict[int, int] = defaultdict(int)
for i, card in enumerate(lines):
    num_cards[i] += 1
    start = i + 1
    end = start + NUM_WINS[i]
    for i_ in range(start, end):
        num_cards[i_] += num_cards[i]

print(sum(num_cards.values()))
