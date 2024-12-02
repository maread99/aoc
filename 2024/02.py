"""Day 2: Red-Nosed Reports

part a: 14mins
part b: 59mins
Initially, for unsafe lines I tried returning the index value where they
were unsafe and checked if they were safe if the value at that index or the
next index were removed. Got caught out by this approach failing to catch
those lines that start ascending/descending and are unsafe by the third
value (index 2) on this basis, but which can be made safe by removing the
first value (index 0) and treating as descending/ascending respectively.
This became apparent when I stopped trying to optimise and just forced it
by checking if each line could be made safe by removing any single index
(as the solution here). Given the short length of each line, I should have
forced it earlier. The initial approach could have been made good by also
checking if an unsafe line could be made safe by removing the index
immediately prior to the unsafe index.

total: 73mins, 15.5x bottom of the leaderboard.

#lists
"""

import itertools
from aocd import get_data


raw = get_data(day=2, year=2024)

# raw = """7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9
# """


lines = [list(map(int, l.split(" "))) for l in raw.splitlines()]


def is_safe(line: list) -> bool:
    ascending = True if line[1] > line[0] else False
    for a, b in itertools.pairwise(line):
        if ascending and b < a + 1 or b > a + 3:
            return False
        elif not ascending and b > a - 1 or b < a - 3:
            return False
    return True


print(sum(is_safe(line) for line in lines))


count = 0
for line in lines:
    safe = is_safe(line)
    if not safe:
        for i in range(len(line)):
            line_ = line.copy()
            del line_[i]
            safe = is_safe(line_)
            if safe:
                break
    if safe:
        count += 1
print(count)
