"""Day 2: Rock Paper Scissors"""

from aocd import get_data

raw = get_data(day=2, year=2022)

data = raw.split("\n")

# treat all hands in terms of A, B, C
losing_results = (
    ["A", "C"],
    ["C", "B"],
    ["B", "A"],
)

hand_score = {"A": 1, "B": 2, "C": 3}


def rnd_result(rnd: list[str]) -> int:
    """Get round score. Example `rnd` ["A", "C"]."""
    res = 6
    if rnd in losing_results:
        res = 0
    elif rnd[0] == rnd[1]:
        res = 3
    res += hand_score[rnd[1]]
    return res


mapping = {"X": "A", "Y": "B", "Z": "C"}

total = 0
for rnd in data:
    rnd = rnd.split()
    rnd[1] = mapping[rnd[1]]
    total += rnd_result(rnd)

print(total)


losing_mapping = dict(losing_results)
winning_mapping = dict(zip(losing_mapping.values(), losing_mapping.keys()))


def get_hand(other: str, code: str) -> str:
    """Return hand to play to get result `code` when other has `other`."""
    if code == "X":
        return losing_mapping[other]
    elif code == "Z":
        return winning_mapping[other]
    return other


data = raw.split("\n")

total = 0
for rnd in data:
    other, code = rnd.split()
    hand = get_hand(other, code)
    total += rnd_result([other, hand])
print(total)
