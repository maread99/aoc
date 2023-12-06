"""Day 6: Wait For It

part a: 28mins (including an embarrassingly careless oversight)

part b: 37mins I clearly need to work on my appreciation of execution times
for different types of operations. I fell head first into the trap that had
been laid by the previous puzzles. On seeing seemingly large inputs I dived
into a binary search without bothering to consider that the size might
still permit the part a approach which would have been far slower to
execute, but quick enough and disproportionately quicker to implement...

total: 65mins, 13x bottom of the leaderboard.
"""

from aocd import get_data

raw = get_data(day=6, year=2023)

lines = raw.splitlines()

times = lines[0].split(":")[1].split()
distances = lines[1].split(":")[1].split()
races = [(int(t), int(d)) for t, d in zip(times, distances)]


def race_won(t, d, a):
    time_remaining = t - a
    dist_travelled = time_remaining * a
    return dist_travelled > d


# part a

wins = 1
for t, d in races:
    count = 0
    for a in range(1, t):
        if race_won(t, d, a):
            count += 1
    wins *= count

print(wins)

# part b
T = int("".join(times))
D = int("".join(distances))

# What I should have done... 8 seconds to execute!
# count = 0
# for a in range(1, T):
#     if race_won(T, D, a):
#         count += 1
# print(count)

# what i did do... 😳


def get_bound(initial: tuple[int, int], go_left=True):
    """Get the first (`go_left` True) or last winning value."""
    seen = {initial}
    bounds = initial

    def get_next_bound(bounds):
        mid = ((bounds[1] - bounds[0]) // 2) + bounds[0]
        if race_won(T, D, mid) == go_left:
            return (bounds[0], mid)
        else:
            return (mid, bounds[1])

    while (new_bounds := get_next_bound(bounds)) not in seen:
        seen.add(new_bounds)
        bounds = new_bounds

    if go_left:
        return bounds[1]
    return bounds[0]


left_bound = get_bound((0, T), go_left=True)
right_bound = get_bound((0, T), go_left=False)
wins = right_bound - left_bound + 1
print(wins)
