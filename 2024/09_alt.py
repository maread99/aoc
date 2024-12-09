"""Day 9: Disk Fragmenter

This is how I could have got my initial approach to work (see doc for
`09.py`). This would have been much quicker to write and execution's
just as quick (couple of seconds).

#strings
"""

import itertools

from aocd import get_data


raw = get_data(day=9, year=2024)

# raw = "2333133121414131402"

FREE = chr(len(raw) // 2 + 2)


def get_disk(disk_map: str) -> str:
    s = ""
    for i, (size, free) in enumerate(itertools.batched(raw[:-1], 2)):
        s += chr(i) * int(size)
        s += FREE * int(free)
    s += chr(i + 1) * int(raw[-1])
    return s


# part_a

disk = get_disk(raw)
while FREE in disk:
    disk = disk.replace(FREE, disk[-1], count=1)[:-1]

print(sum(i * ord(blk) for i, blk in enumerate(disk)))


# part b
s = get_disk(raw)
new = ""

while s:
    blk = s[-1]
    if blk == FREE:
        new = blk + new
        s = s[:-1]
        continue
    file = blk
    for blk in s[::-1][1:]:
        if blk == file[-1]:
            file += blk
        else:
            break
    size = len(file)
    if FREE * size in s:
        s = s.replace(FREE * size, file, count=1)
        new = FREE * size + new
    else:
        new = file + new
    s = s[:-size]

print(sum(ord(c) * i for i, c in enumerate(new) if c != FREE))
