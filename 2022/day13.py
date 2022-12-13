"""Day 13: Distress Signal

Part a: 95mins writting an unnecessarily over complicated version of what
ended up as `in_order`.

Parb b: nearly 2hrs after looking at the simple example data and trying
to solve by sorting according to the first int of each line and then using
regexes to position the markers within their relevant group (then adding
the number of lines in the lower groups). Although I attributed lines with
no ints to group 0, failed to recognise that any line which has an empty
list as the first evaluated value will be ordered ahead of those that
don't, such that the correct order of the following is:
    '[[[[],9,[8,8,9,10,9]],[],10,10],[10,[],0]]',
    '[[0],[],[5],[4,7]]',
(If such lines are assigned to group 0 then this approach does work.)

Thinking the issue was with positioning markers within groups, tried
using `in_order` to just order the marker groups (wrongly assumed it would
take too long to sort the whole 300 lines). Failed as the grouping on the
basis of the first integer was still flawed. (NB, as it was the markers
were positioned at the start of each 'group', at least in my data, although
they could have fallen later, for example '[[2]]' would be ordered after
'[2, 3, 4]'.)

Relaised it wouldn't actually take that long to simply sort the lot via
`in_order` (although pretty sure there must be a better to do this than how
I've implemneted it here. EDIT: of course there is, see revision).
"""

from aocd import get_data

raw = get_data(day=13, year=2022)

data = [pair.splitlines() for pair in raw.split("\n\n")]


def in_order_(left: int | list[int], right: int | list[int]) -> bool | None:
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    for l_, r in zip(left, right):
        if isinstance(l_, int) and isinstance(r, int):
            if l_ == r:
                continue
            return l_ < r
        if isinstance(l_, int):
            l_ = [l_]
        if isinstance(r, int):
            r = [r]
        ordered = in_order_(l_, r)
        if ordered is not None:
            return ordered

    # tie
    if len(left) == len(right):
        return None
    return len(left) < len(right)


def in_order(left: int | list[int], right: int | list[int]) -> bool:
    ordered = in_order_(left, right)
    return True if ordered is None else ordered


t = 0
for i, pair in enumerate(data):
    t += i + 1 if in_order(eval(pair[0]), eval(pair[1])) else 0
print(t)

# part b

data = raw.replace("\n\n", "\n").splitlines()
markers = ["[[2]]", "[[6]]"]
data += markers

# There has to be a better way to sort a list according to a function that
# compares any two values?
idxs = []
for i, line in enumerate(data):
    line = eval(line)
    idxs.append(
        sum(not in_order(line, eval(other)) for i_, other in enumerate(data) if i != i_)
    )
srtd = sorted(data, key=lambda x: idxs[data.index(x)])
print((srtd.index(markers[0]) + 1) * (srtd.index(markers[1]) + 1))
