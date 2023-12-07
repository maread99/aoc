"""Day 7: Camel Cards

This version sorts with an absolute key function.
See 07_rev for the better comparision function version...

The sort based on absolute key values is quicker than the comparison
version, but we're only talking a second or so given the relatively short
list length.

part a: 61mins
Really annoying. Originally implemented the sort key as a comparision
function although couldn't get it working. Switched to a standard
function that resolved the evaluation 'in event of a tie' by adding a
decimal value to the rank and returning as a float (the version here).
Only then realised that the problem had been in the ranking function rather
than the way the comparison function had been implmented. Lost loads of
time with the unnecessary change of approach.

part b: 68mins
Lost time identifying a bug in the wildcard inputs. Bug due to evaluating
the non jokers as what was left in a set, which had the effect of treating
duplicates of other cards as jokers as well 😳.

total: 129, 8x bottom of the leaderboard.
"""

from aocd import get_data

raw = get_data(day=7, year=2023)

# lines = """32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483""".splitlines()

lines = raw.splitlines()

MAP = {
    "T": "10",
    "J": "11",
    "Q": "12",
    "K": "13",
    "A": "14",
}


def get_hand_rank(line: str):
    h = line.split()[0]
    st = set(h)

    decimal_ = "0." + "".join(["0" + c if c.isdigit() else MAP[c] for c in h])
    decimal = float(decimal_)

    if len(st) == 1:
        return 6 + decimal
    if len(st) == 2 and h.count(h[0]) in (1, 4):
        return 5 + decimal
    if len(st) == 2 and h.count(h[0]) in (2, 3):
        return 4 + decimal
    # bug: generator object with True bool representation, not False for empty sequence
    # if (len(st)) == 3 and (c for c in st if h.count(c) == 3):
    if (len(st)) == 3 and any((c for c in st if h.count(c) == 3)):  # corrected
        return 3 + decimal
    if (len(st)) == 3 and any((c for c in st if h.count(c) == 2)):  # corrected
        return 2 + decimal
    if (len(st)) == 5:
        return 0 + decimal
    return 1 + decimal


lines.sort(key=get_hand_rank)

total = 0
for i, line in enumerate(lines):
    bid = int(line.split()[1])
    total += (i + 1) * bid

print(total)

# part b

lines = raw.splitlines()

MAP = {
    "T": "10",
    "J": "01",
    "Q": "12",
    "K": "13",
    "A": "14",
}


def _get_hand_rank(h: str):
    st = set(h)
    if len(st) == 1:
        return 6
    if len(st) == 2 and h.count(h[0]) in (1, 4):
        return 5
    if len(st) == 2 and h.count(h[0]) in (2, 3):
        return 4
    if (len(st)) == 3 and any((c for c in st if h.count(c) == 3)):
        return 3
    if (len(st)) == 3 and any((c for c in st if h.count(c) == 2)):
        return 2
    if (len(st)) == 5:
        return 0
    return 1


VALUES = "A,K,Q,J,T,9,8,7,6,5,4,3,2".split(",")


def get_hand_rank(line: str):
    h = line.split()[0]
    num_j = h.count("J")

    rank = None
    if not num_j:
        rank = _get_hand_rank(h)

    if h.count("J") in (5, 4):
        rank = 6

    if rank is None:
        rank = 0
        # bug resulting in treating duplicates of other cards as jokers as well 😳...
        # others = "".join(st - {"J"})
        others = "".join([c for c in h if c != "J"])  # corrected
        hands = new_hands = [others]
        while len(new_hands[0]) != 5:
            new_hands = []
            for hand in hands:
                for v in VALUES:
                    new_hands.append(hand + v)
            hands = new_hands
        for hand in hands:
            rank = max(rank, _get_hand_rank(hand))

    decimal_ = "0." + "".join(["0" + c if c.isdigit() else MAP[c] for c in h])
    decimal = float(decimal_)
    return rank + decimal


lines.sort(key=get_hand_rank)

total = 0
for i, line in enumerate(lines):
    bid = int(line.split()[1])
    total += (i + 1) * bid

print(total)
