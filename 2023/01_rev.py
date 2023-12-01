"""Day 1: Trebuchet?!

Of course should have just used isdigit for part a...
"""

from aocd import get_data

raw = get_data(day=1, year=2023)
lines = raw.splitlines()

total = 0
for line in lines:
    ints = [c for c in line if c.isdigit()]
    total += int(ints[0] + ints[-1])

print(total)

# part b (unchanged from original solution)

WORDS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
WORDS_REV = {k[::-1]: v for k, v in WORDS.items()}


def get_value(line: str, words: dict[str, str]) -> str:
    for i, c in enumerate(line):
        if c.isdigit():
            return c
        for word in words:
            if line[i:].startswith(word):
                return words[word]
    raise ValueError(f"val not found for line '{line}'")


left_values = [get_value(line, WORDS) for line in lines]
right_values = [get_value(line[::-1], WORDS_REV) for line in lines]

valves = []
for left, right in zip(left_values, right_values):
    valves.append(int(left + right))

print(sum(valves))
