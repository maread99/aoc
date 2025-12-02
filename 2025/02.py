"""Day 2: Gift Shop

part a: 30mins
Completely overcomplicated it by, again, misreading and thinking that the
pattern could repeat any number of times rather than just twice, i.e. I
solved part b first...

part b: 1min

total: 31mins
14500
#patterns #iteration
"""

import itertools

from aocd import get_data

raw = get_data(day=2, year=2025)

# raw = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

ranges_ = [tuple(map(int, rng.split("-"))) for rng in raw.split(",")]
ranges = [range(rng[0], rng[1] + 1) for rng in ranges_]

# part 1
total = 0

for rng in ranges:
    for v_ in rng:
        v = str(v_)
        ln = len(v)
        if ln % 2:
            continue
        l = v[: (ln // 2)]
        r = v[ln // 2 :]
        if l == r:
            total += v_

print(total)

# part 2
total = 0

for rng in ranges:
    for v_ in rng:
        v = str(v_)
        for i in range(1, (len(v) // 2) + 1):
            if len(v) % i:
                continue  # ID len not mutiple of pattern len
            it = itertools.batched(v, i, strict=True)
            if len(set(it)) == 1:
                total += v_
                break

print(total)
