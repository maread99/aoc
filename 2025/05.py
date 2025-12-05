"""Day 5: Cafeteria

part 1: 10mins
Silly parsing bug. Even sillier that didn't catch it quicker.

part 2: 65mins
I initially massively overcomplicated this by trying to build up a list of
non-overlapping intervals by adding one range at a time. It was while
writting the bit to consolidate overlapping intervals in this list that
I realised this was actually all I needed to do to the ranges in the first
place 🙄.

I've left the initial monstrosity commented out at the bottom.

total: 75mins
16006
#intervals
"""

from aocd import get_data

# raw = get_data(day=5, year=2025)

raw = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

ranges_, ids = raw.split("\n\n")
ranges = [tuple(map(int, rng.split("-"))) for rng in ranges_.splitlines()]

# part 1
count = 0
for v in map(int, ids.splitlines()):
    for rng in ranges:
        if rng[0] <= v <= rng[1]:
            count += 1
            break
print(count)


# part 2
ranges.sort()
intervals = []
current = ranges[0]
for rng in ranges[1:]:
    if current[1] < rng[0]:
        intervals.append(current)
        current = rng
        continue
    if current[1] > rng[1]:
        continue
    current = (current[0], rng[1])
intervals.append(current)

print(sum([b - a + 1 for a, b in intervals]))


# initial part 2 monstrosity

# intervals = [ranges[0]]
# for rng in ranges[1:]:
#     it_intervals = iter(intervals)
#     nintervals = []
#     added = False
#     for intrvl in it_intervals:
#         if rng[1] < intrvl[0] or rng[0] > intrvl[1]:  # doesn't overlap
#             nintervals.append(intrvl)
#             continue
#         if rng[0] <= intrvl[0] and intrvl[1] <= rng[1]:  # rng fully overlaps intrvl
#             nintervals.append(rng)
#             added = True
#             break
#         if intrvl[0] <= rng[0] and rng[1] <= intrvl[1]:  # rng fully overlapped by intrvl
#             nintervals.append(intrvl)
#             added = True
#             break
#         if rng[0] <= intrvl[0] and rng[1] <= intrvl[1]:
#             nintervals.append((rng[0], intrvl[1]))
#             added = True
#             break
#         if intrvl[0] <= rng[0] and intrvl[1] <= rng[1]:
#             nintervals.append((intrvl[0], rng[1]))
#             added = True
#             break
#         assert False, f"shouldn't by reachable!\n{intrvl=}\n{rng=}, "
#     rem = list(it_intervals)
#     if rem:
#         nintervals += rem
#     if not added:
#         nintervals += [rng]
#     nintervals.sort()
#     intervals = nintervals

# # the only idea that's actually needed and was needed here anyway...
# intervals = []
# current = nintervals[0]
# for nintrvl in nintervals[1:]:
#     if current[1] < nintrvl[0]:
#         intervals.append(current)
#         current = nintrvl
#         continue
#     if current[1] > nintrvl[1]:
#         continue
#     current = (current[0], nintrvl[1])
# intervals.append(current)

# print(sum([b - a + 1 for a, b in intervals]))
