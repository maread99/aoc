"""Day 8: Treetop Tree House

2 hours!
"""

from aocd import get_data
import numpy as np

raw = get_data(day=8, year=2022)
data = [[int(v) for v in line] for line in raw.splitlines()]

arr = np.array(data)
res = np.zeros(arr.shape, dtype="int")
ROWS, COLS = arr.shape

for i in range(COLS):
    if i in {0, COLS - 1}:
        res[:, i] = 1
        continue
    bv = arr[:, :i].max(axis=1) < arr[:, i]  # look from left
    res[:, i] += bv
    bv = arr[:, -i:].max(axis=1) < arr[:, -i - 1]  # look from right
    res[:, -i - 1] += bv

for j in range(ROWS):
    if j in {0, ROWS - 1}:
        res[j, :] = 1
        continue
    bv = arr[:j, :].max(axis=0) < arr[j, :]  # look down from top
    res[j, :] += bv
    bv = arr[-j:, :].max(axis=0) < arr[-j - 1, :]  # look up from bottom
    res[-j - 1, :] += bv

print((res > 0).sum(axis=None))


def num_trees(h, sub: np.ndarray) -> int:
    """Return number of trees visible along subarray."""
    bv = sub >= h
    return len(bv) if not bv.any() else bv.argmax() + 1


v_max = 0
for j in range(1, ROWS - 2):  # scenic view is 0 on edges as * 0
    for i in range(1, COLS - 2):
        h = arr[(j, i)]
        v = 1
        v *= num_trees(h, np.flip(arr[:j, i]))  # look up
        v *= num_trees(h, arr[j + 1 :, i])  # look down
        v *= num_trees(h, np.flip(arr[j, :i]))  # look left
        v *= num_trees(h, arr[j, i + 1 :])  # look right
        v_max = max(v_max, v)
print(v_max)
