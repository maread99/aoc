"""Day 3: Mull It Over

The regex version that I should have done in the first place.

I like the splitting of the do and don't although an alternative is to
include these terms within the regex and toggle a flag when either appear,
then only add the value to the total if the flag is enabled. For an example
of this see:
    https://github.com/mebeim/aoc/blob/master/2024/original_solutions/day03.py

#regex
"""

import math
import re

from aocd import get_data


raw = get_data(day=3, year=2024)

# raw = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

regex = re.compile(r"mul\(\d+,\d+\)")

matches = regex.findall(raw)
vals = [math.prod(map(int, match[4:-1].split(","))) for match in matches]
print(sum(vals))

# raw = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

lines = [l.split("don't()")[0] for l in raw.split("do()")]
total = 0
for line in lines:
    matches = regex.findall(line)
    total += sum(math.prod(map(int, match[4:-1].split(","))) for match in matches)

print(total)
