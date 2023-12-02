"""Day 1: Trebuchet?!

part a: 9mins
part b: 29mins, changed approach.
total: 38 mins, 5.4x bottom of the leaderboard.

Feeling rusty.
"""

import re

from aocd import get_data

raw = get_data(day=1, year=2023)
lines = raw.splitlines()

valves = []
for line in lines:
    # regex from `helpers.utils.ints`. extracts ints from a string
    vals = re.findall(r"(?:(?<!\d)-)?\d+", line)
    valve = vals[0][0] + vals[-1][-1]
    valves.append(int(valve))

print(sum(valves))

# part b

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
WORDS_REV = {k[-1::-1]: v for k, v in WORDS.items()}


def get_value(line: str, words: dict[str, str]) -> str:
    for i, c in enumerate(line):
        if c.isdigit():
            return c
        for word in words:
            if line[i:].startswith(word):
                return words[word]
    raise ValueError(f"val not found for line '{line}'")


left_values = [get_value(line, WORDS) for line in lines]
right_values = [get_value(line[-1::-1], WORDS_REV) for line in lines]

valves = []
for left, right in zip(left_values, right_values):
    valves.append(int(left + right))

print(sum(valves))
