"""Day 5: If You Give A Seed A Fertilizer

Having looked around, the basis of my original implementation is the way
to do it, although I had indeed over complicated it. That said, I was
surprised how many of the features I'd incorporated were part of the
cleaner solution (albeit cleaner!).

The key simplification is evaluating the overlaps - just evaluate where the
source range fully overlaps the destination range and chuck any parts
either side back in the mix to be considered again against any other
mappings or, as applic, from where they will be let through as is.

Wrote the following after seeing hyper-neutrino's very succient solutions:
https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day05p1.py
https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day05p2.py
What's below is pretty much the same...
"""

from aocd import get_data

raw = get_data(day=5, year=2023)

# part a
seeds, *blocks = raw.split("\n\n")
seeds = list(map(int, seeds.split(":")[1].split()))

for block in blocks:
    rngs = [list(map(int, rng.split())) for rng in block.split("\n")[1:]]
    new = []
    for v in seeds:
        for start_d, start_s, length in rngs:
            if start_s <= v < start_s + length:
                new.append(start_d + (v - start_s))
                break
        else:
            new.append(v)
    seeds = new

print(min(seeds))

# part b

inputs, *blocks = raw.split("\n\n")
inputs = list(map(int, inputs.split(":")[1].split()))

seeds = []
for i in range(0, len(inputs), 2):
    # have right of seed ranges as 'stop' rather than end
    seeds.append([inputs[i], inputs[i] + inputs[i + 1]])

for block in blocks:
    rngs = [list(map(int, rng.split())) for rng in block.split("\n")[1:]]

    new = []
    while seeds:
        s, e = seeds.pop()
        for sd, ss, length in rngs:
            overlap_start = max(s, ss)
            overlap_end = min(e, ss + length)
            # handle the fully overlapped part here, chuch the rest back in the mix
            if overlap_start < overlap_end:
                # sd - ss is the required shift for mapping (diff in original version)
                new.append([overlap_start + sd - ss, overlap_end + sd - ss])
                if s < overlap_start:
                    seeds.append([s, overlap_start])
                if e > overlap_end:
                    seeds.append([overlap_end, e])
                break
        else:
            new.append([s, e])

    seeds = new

print(min(new)[0])
