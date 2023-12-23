"""Day 22: 

part a: 1hr 55
Annoyingly had couple of bugs about issues that I'd considered yet failed
to account for within all parts of the implementation (including not
confusing a vertical block falling on 'itself' as having hit another
block).

part b: 1hr 50
Execution takes about 40secs.
Managed to realise and accommodate the initial oversight of counting the
same block multiple times if it were to fall more than once. Not that I'm
sure how that could even happen.

total: 3hrs 45, 7.5x bottom of the leaderboard.

#sets
"""

import copy
from collections import deque

from aocd import get_data

raw = get_data(day=22, year=2023)

# raw = """1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9
# """

lines = raw.splitlines()

Block = set[tuple[int, int, int]]  # tuples of x, y, z
Cells = set[tuple[int, int, int]]  # tuples of x, y, z

# Evaluate blocks in original positions
BLOCKS_ORIG: list[Block] = []

for line in lines:
    block: Block = set()
    s, e = line.split("~")
    sx, sy, sz = [int(v) for v in s.split(",")]
    ex, ey, ez = [int(v) for v in e.split(",")]
    if sx != ex:
        for i in range(min(sx, ex), max(sx, ex) + 1):
            block.add((i, sy, sz))

    elif sy != ey:
        for i in range(min(sy, ey), max(sy, ey) + 1):
            block.add((sx, i, sz))

    elif sz != ez:
        for i in range(min(sz, ez), max(sz, ez) + 1):
            block.add((sx, sy, i))
    else:
        block.add((sx, sy, sz))

    BLOCKS_ORIG.append(block)

BLOCKS_ORIG.sort(reverse=True, key=lambda block: max(z for _, _, z in block))

# Evaluate blocks at rest

BLOCKS_CELLS: Cells = set()
BLOCKS: list[Block] = []
while BLOCKS_ORIG:
    block = BLOCKS_ORIG.pop()
    while not any(z == 1 for _, _, z in block):
        nblock = {(x, y, z - 1) for x, y, z in block}
        if BLOCKS_CELLS & nblock:
            break
        block = nblock
    BLOCKS.append(block)
    BLOCKS_CELLS |= block


def would_drop(block: Block, blocks_cells: Cells) -> bool:
    """Query if block would drop given `blocks_cells`."""
    remaining_cells = blocks_cells - block
    for x, y, z in block:
        if z == 1:
            return False
        if (x, y, z - 1) in remaining_cells:
            return False
    return True


# part a

count = 0
for block in BLOCKS:
    for x, y, z in block:
        one_up = (x, y, z + 1)
        if (one_up not in block) and (one_up in BLOCKS_CELLS):
            block_above = next(block_ for block_ in BLOCKS if one_up in block_)
            if would_drop(block_above, BLOCKS_CELLS - block):
                count += 1
                break


print(len(BLOCKS) - count)


# part b

counts = []
for i in range(len(BLOCKS)):
    blocks = copy.deepcopy(BLOCKS)
    blocks_cells = BLOCKS_CELLS.copy()
    blocks_to_remove = deque([(blocks[i], i)])
    idxs: set[int] = set()
    while blocks_to_remove:
        block, idx = blocks_to_remove.popleft()
        idxs.add(idx)
        blocks_cells -= block
        blocks_above: list[int] = []
        for x, y, z in block:
            one_up = (x, y, z + 1)
            if one_up in blocks_cells:
                idx = next(idx for idx, block_ in enumerate(blocks) if one_up in block_)
                if idx not in blocks_above:
                    blocks_above.append(idx)
        for idx in blocks_above:
            block_above = blocks[idx]
            if would_drop(block_above, blocks_cells):
                space_above = block_above.copy()
                block = block_above
                while not any(z == 1 for _, _, z in block):
                    nblock = {(x, y, z - 1) for x, y, z in block}
                    if blocks_cells & nblock:
                        break
                    block = nblock
                # Necessary to use the set for the original block so that the blocks as
                # defined in `blocks` are dynamically update to new positions.
                block_above.clear()
                block_above |= block
                blocks_cells |= block_above
                blocks_to_remove.append((space_above, idx))
    counts.append(len(idxs))

print(sum([c - 1 for c in counts]))
