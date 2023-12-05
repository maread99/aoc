"""Day 5: If You Give A Seed A Fertilizer

What is happening with the difficulty in the early days this year! It's
yo-yoing like crazy and has peaked (so far) with part b of this one.

part a: 50mins. First implemented as a mapping beteen directories that
covered all the values. Worked for the example, 😏. Did not appreciate the
size and range of the values of the actual inputs. Lesson (taken previously
but not learnt) - LOOK AT THE ACTUAL INPUTS FIRST!

part b: 6hrs 40mins!
Spent too long with a failed approach that I didn't sufficiently think
through before ploughing into it.

Got it out in the end with an implementation that was doublessly
unnecessarily complex, although believe that the basis is sound -
evaluating ranges of original values that map to values with a constant
difference in the final values. Spent an age refining / debugging.

total: 7.5hrs, 17x bottom of the leaderboard (27mins).
"""

import pandas as pd
from aocd import get_data

raw = get_data(day=5, year=2023)

lines = raw.split("\n\n")

# part a

seeds = list(map(int, lines[0].split(":")[1].split()))
seed = seeds[0]

all_converters = []
for line in lines[1:]:
    info_parts = line.split("\n")[1:]
    all_converters.append([list(map(int, part.split())) for part in info_parts])

def get_mapped_value(converter: list[list[int]], value: int) -> int:
    for start_d, start_s, length in converter:
        if start_s <= value < start_s + length:
            return start_d + (value - start_s)
    return value

outcomes = []
for seed in seeds:
    value = seed
    for converter in all_converters:
        value = get_mapped_value(converter, value)
    outcomes.append(value)

print(min(outcomes))

# part b

Rng = tuple[pd.Interval, int]
CLOSED = "both"


def converter_to_ranges(converter: list[list[int]]) -> list[Rng]:
    """Return a converter (input for a specific map) to 'ranges'
    
    Ranges returned as a list[tuple[pd.Interval, int]] where each item of
    list represents a range within the full scope of the mappings for the
    specific `converter`. Each item is a tuple where the pd.Interval
    describes the extent of the range covered and the int describes the
    difference between the mapped values for this part of the range (and
    for the specific mapping represented by the `converter`).
    """
    rngs: list[tuple[pd.Interval, int]] = []  # where tuple[interval, diff to end]
    for start_d, start_s, length in converter:
        rngs.append(
            (pd.Interval(start_s, start_s + length - 1, CLOSED), start_d - start_s)
        )
    rngs.sort(key=lambda x: (x[0].left, x[0].right))
    return rngs


def update_rng(rng_a: Rng, rng_b: Rng) -> list[Rng]:
    """Update an original range that overlaps with a range in a later mapping."""
    (a, a_diff), (b, b_diff) = rng_a, rng_b
    assert a.overlaps(b)

    if a == b:
        return [(a, a_diff + b_diff)]

    if a.left < b.left and a.right > b.right:
        # fully overlaps
        return [
            (pd.Interval(a.left, b.left - 1, CLOSED), a_diff),
            (b, a_diff + b_diff),
            (pd.Interval(b.right + 1, a.right, CLOSED), a_diff),
        ]

    if a.left < b.left:
        return [
            (pd.Interval(a.left, b.left - 1, CLOSED), a_diff),
            (pd.Interval(b.left, a.right, CLOSED), a_diff + b_diff),
        ]

    # a.left >= b.left
    if a.right > b.right:
        return [
            (pd.Interval(a.left, b.right, CLOSED), a_diff + b_diff),
            (pd.Interval(b.right + 1, a.right, CLOSED), a_diff),
        ]

    # a fully overlapped by b
    return [(pd.Interval(a.left, a.right, CLOSED), a_diff + b_diff)]


def adjust_rngs(rngs: list[Rng], adj: int) -> list[Rng]:
    """Adjust `rngs` by `adj` to be on the same terms as a different mapping."""
    return [
        (pd.Interval(intrvl.left + adj, intrvl.right + adj, CLOSED), diff)
        for intrvl, diff in rngs
    ]

# evaluate ranges that map seeds to location with a constant difference
all_rngs = converter_to_ranges(all_converters[0])
for i, converter in enumerate(all_converters[1:]):
    rngs_nxt = converter_to_ranges(converter)

    new = []
    while all_rngs:
        rng = all_rngs.pop(0)
        intrvl, diff = rng
        adj_rngs = adjust_rngs(rngs_nxt, -diff)
        stack = [rng]
        while stack:
            rng_ = stack.pop(-1)
            for adj_rng in adj_rngs:
                if rng_[0].overlaps(adj_rng[0]):
                    new_rngs = update_rng(rng_, adj_rng)
                    if rng_[0].right > adj_rng[0].right:
                        # send it back through
                        stack.append(new_rngs[-1])
                        new.extend(new_rngs[:-1])
                    else:
                        new.extend(new_rngs)
                    break

    all_rngs = new

# map seed values for the first and last of each mapping range that the
# range of seeds overlaps, and extract minimum of these mapped values.
min_ = float("inf")
for i in range(0, len(seeds), 2):
    seed_rng_s, length = seeds[i : i + 2]
    seed_rng = pd.Interval(seed_rng_s, seed_rng_s + length - 1, CLOSED)
    for intrvl, diff in all_rngs:
        if seed_rng.overlaps(intrvl):
            seed_left = max(seed_rng.left, intrvl.left)
            min_ = min((min_, seed_left + diff))
            seed_right = min(seed_rng.right, intrvl.right)
            min_ = min((min_, seed_right + diff))

print(min_)
