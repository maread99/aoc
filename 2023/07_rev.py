"""Day 7: Camel Cards

How I'd started and was intending to implement it...
"""

from functools import cmp_to_key

from aocd import get_data

raw = get_data(day=7, year=2023)

# lines = """32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483""".splitlines()

lines = raw.splitlines()


def get_hand_rank(line: str):
    h = line.split()[0]
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


# part a

MAP_A = {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def comp_func(a_: str, b_: str) -> int:
    a = a_.split()[0]
    b = b_.split()[0]
    rank_a = get_hand_rank(a)
    rank_b = get_hand_rank(b)
    if rank_a != rank_b:
        return -1 if rank_a < rank_b else 1
    for ac_, bc_ in zip(a, b):
        ac = int(ac_) if ac_.isdigit() else MAP_A[ac_]
        bc = int(bc_) if bc_.isdigit() else MAP_A[bc_]
        if ac == bc:
            continue
        return -1 if ac < bc else 1
    assert False, (a, b)


lines.sort(key=cmp_to_key(comp_func))

total = 0
for i, line in enumerate(lines):
    bid = int(line.split()[1])
    total += (i + 1) * bid

print(total)

# part b

MAP_B = {
    "T": 10,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
}

VALUES = "A,K,Q,T,9,8,7,6,5,4,3,2".split(",")


def get_hand_rank_b(line: str) -> int:
    h = line.split()[0]
    num_j = h.count("J")

    rank = None
    if not num_j:
        rank = get_hand_rank(h)

    if h.count("J") in (5, 4):
        rank = 6

    if rank is None:
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


def comp_func_b(a_: str, b_: str) -> int:
    a = a_.split()[0]
    b = b_.split()[0]
    rank_a = get_hand_rank_b(a_)
    rank_b = get_hand_rank_b(b_)
    if rank_a != rank_b:
        return -1 if rank_a < rank_b else 1
    for ac_, bc_ in zip(a, b):
        ac = int(ac_) if ac_.isdigit() else MAP_B[ac_]
        bc = int(bc_) if bc_.isdigit() else MAP_B[bc_]
        if ac == bc:
            continue
        return -1 if ac < bc else 1
    assert False, (a, b)


lines.sort(key=cmp_to_key(comp_func_b))

total = 0
for i, line in enumerate(lines):
    bid = int(line.split()[1])
    total += (i + 1) * bid

print(total)
