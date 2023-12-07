"""Day 7: Camel Cards

Inspried by hyper-neutrino (and others):
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day07p1.py

Uses Counter and structural pattern matching for the ranking function.
Sorts with key as an absolute function returning a 2-tuple, first item
defines hand rank, second how to resolve a tie. Tie resolved by absolute
value of card given that "A" > "9" (requires first mapping 'letter cards').

#codify-rules  #sort  #counting  #stuctural-pattern-matching
"""

from collections import Counter

from aocd import get_data

raw = get_data(day=7, year=2023)

# lines = """32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483""".splitlines()

lines = raw.splitlines()


def get_hand_rank(line: str) -> int:
    hand = line.split()[0]
    match sorted(Counter(hand).values(), reverse=True):
        case [5]:
            return 6
        case [4, 1]:
            return 5
        case [3, 2]:
            return 4
        case [3, 1, 1]:
            return 3
        case [2, 2, 1]:
            return 2
        case [2, *_]:
            return 1
        case [1, 1, 1, 1, 1]:
            return 0
    assert False, hand


# part a

assert "A" > "9"
MAP = {
    "T": "A",
    "J": "B",
    "Q": "C",
    "K": "D",
    "A": "E",
}

lines_ = sorted(lines, key=lambda x: (get_hand_rank(x), [MAP.get(c, c) for c in x]))
total = 0
for i, line in enumerate(lines_):
    bid = int(line.split()[1])
    total += (i + 1) * bid

print(total)

# part b

VALUES = "A,K,Q,T,9,8,7,6,5,4,3,2".split(",")


def get_hand_rank_b(line: str) -> int:
    h = line.split()[0]
    rank = 0
    others = "".join([c for c in h if c != "J"])
    hands = new_hands = [others]
    while len(new_hands[0]) != 5:
        new_hands = []
        for hand in hands:
            for v in VALUES:
                new_hands.append(hand + v)
        hands = new_hands
    for hand in hands:
        rank = max(rank, get_hand_rank(hand))

    return rank


MAP_B = {
    "T": "A",
    "J": "1",
    "Q": "C",
    "K": "D",
    "A": "E",
}
lines_ = sorted(lines, key=lambda x: (get_hand_rank_b(x), [MAP_B.get(c, c) for c in x]))

total = 0
for i, line in enumerate(lines_):
    bid = int(line.split()[1])
    total += (i + 1) * bid

print(total)
