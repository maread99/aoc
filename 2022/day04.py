"""Day 4: Camp Cleanup"""

from aocd import get_data

raw = get_data(day=4, year=2022)
data = raw.splitlines()


def get_sections(section_data: str) -> set[int]:
    start, end = [int(v) for v in section_data.split("-")]
    return set(range(start, end + 1))


# using sets for part a is a bit overkill. Could have just compared the
# range extremes to see if either overlap the other, although using sets
# was a good bet on part b requiring them.
count = 0
for line in data:
    a, b = line.split(",")
    a_, b_ = get_sections(a), get_sections(b)
    if a_.issubset(b_) or b_.issubset(a_):
        count += 1
print(count)


count = 0
for line in data:
    a, b = line.split(",")
    a_, b_ = get_sections(a), get_sections(b)
    if a_ & b_:
        count += 1
print(count)
