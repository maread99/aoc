"""Day 9: Disk Fragmenter

part a: 47mins
I don't think I ever really got to grips with this problem until after I'd
solved it. My initial attempt involved manipulating a string. Worked fine
for the example but was never going to work on the real data were ID values
go to into double digits. (A single character, for example '4', can
represent both the space a block represents (1 space) and that block's id
value, but whilst '14' can represent an id value, it takes up 2 spaces,
where a block can only take up one. I've just realised that I could have
made this approach work by using `chr` to convert id values into a 1-length
strings. I'll write it up to `09_alt.py`).

part b: 2hours 10 minutes
Unbelievably, for some reason I thought I could get away with string
manipulation again. Again worked on the example, again failed on the real
data for the same reason as it didn't work before. (And again I could have
got it to work if I'd simply used `chr`. See `09_alt.py`)

When I did get part b written I spent a decent while debugging because
I'd stupidly left in something hardcoded to the example data (worked for
the example!)

total: 2hours 57 minutes, 12.6x bottom of the leaderboard.

I'm not sure I like the way I did it, but it works and it's quick.

#arrays
"""

import itertools
from collections import deque

from aocd import get_data


raw = get_data(day=9, year=2024)

# raw = "2333133121414131402"

FREE = "F"


def get_disk(disk_map: str) -> list[int | str]:
    disk: list[int | str] = []
    for i, (size, free) in enumerate(itertools.batched(disk_map[:-1], 2)):
        disk.extend([i] * int(size))
        disk.extend([FREE] * int(free))
    disk.extend([(i + 1)] * int(disk_map[-1]))
    return disk


def get_free_indexes(disk: list[int | str]) -> deque[int]:
    idxs = deque([])
    for i, v in enumerate(disk):
        if v == FREE:
            idxs.append(i)
    return idxs


# part_a

disk = get_disk(raw)
free_indexes = get_free_indexes(disk)
num_free_indexes = len(free_indexes)

while free_indexes:
    fi = free_indexes.popleft()
    blk = disk.pop()
    while blk == FREE:
        blk = disk.pop()
    if fi > len(disk) - 1:
        disk.append(blk)
        break
    disk[fi] = blk

print(sum(i * blk for i, blk in enumerate(disk)))


# part b

disk = get_disk(raw)
free_indexes = get_free_indexes(disk)
prev_fi = free_indexes[0]
# gaps = [(2, 1)]  # WHAT A bug TO HAVE! Had hard coded the first gap to the example!
gaps = [(prev_fi, 1)]  # gaps with a gap as tuple of (index of gap start, gap length)
for fi in list(free_indexes)[1:]:
    if prev_fi + 1 == fi:  # still in the gap
        gaps[-1] = (gaps[-1][0], gaps[-1][1] + 1)
    else:  # starting a new gap
        gaps.append((fi, 1))
    prev_fi = fi

DISK_LEN = len(disk)

file = [disk[-1]]
for i_rev, blk in enumerate(disk[:-1][::-1]):
    if blk == file[-1]:
        file.append(blk)
        continue
    elif file[-1] == FREE:
        file = [blk]  # start a new file
        continue
    else:
        # move most recent file, if possible
        for ig, gap in enumerate(gaps):
            size = len(file)
            start, space = gap
            if start > DISK_LEN - i_rev:
                break
            if space >= size:
                start_file = -i_rev - 1
                end_file = start_file + size
                if not end_file:
                    end_file = None
                disk[start_file:end_file] = [FREE] * size  # free up old location
                disk[start : start + size] = file  # enter to new location
                # update gap
                if size == space:
                    del gaps[ig]
                else:
                    gaps[ig] = (start + size, space - size)
                break
        file = [blk]

print(sum(i * blk for i, blk in enumerate(disk) if blk != FREE))
