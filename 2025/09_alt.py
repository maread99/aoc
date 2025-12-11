"""Day 9: Movie Theater

This was how I first implmemented it, which actually worked after
correcting a bug in the area calculation (see 09.py).

It evaluates the boundary and from that describes the interior, for
each column, in terms of ranges of the rows that fall inside. Then of all
the possible rectangles only considers those for which each 'up/down' side
falls within an interior range for the corresponding column.
NOTE: I probably got lucky here as only excludes rectangles if either of
the vertical sides of fall outside the interior - it gives no consideration
to the horizontal sides - with different input would certainly be possible
that it sets the max area to a rectangle which should be excluded due to
the 'middle' part of one of the horizontal sides breaching the boundary.

NOTE: Implementation assumes input is such that the path is described as if
walking around in an anti-clockwise direction, i.e. as the example (and at
least my input).

#ranges
"""

from collections import defaultdict

from aocd import get_data

# raw = get_data(day=9, year=2025)

raw = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

lines = [tuple(map(int, line.split(","))) for line in raw.splitlines()]

# part 1
max_ = 0
for i_, (i, j) in enumerate(lines[:-1]):
    for i2, j2 in lines[i_+1:]:
        area = (abs(i2 - i) + 1) * (abs(j - j2 + 1))
        max_ = max_ if max_ > area else area

print(max_)

# part 2

# Describe boundary in terms of columns using dict
#   keys as column index
#   values as list of ranges of all j coordinates on which the boundary
#       falls for that column.
boundary_i: dict[int, list[tuple[int, int], str]] = defaultdict(list)

# NOTE: implementation of corners assumes input is such that the path is
# described as if walking around in an anti-clockwise direction, i.e. as
# the example (and at least my input).
CORNERS_IN = set()
CORNERS_OUT = set()

for it, (i, j) in enumerate(lines):
    pi, pj = (lines[-1][0], lines[-1][1]) if it == 0 else (lines[it-1][0], lines[it-1][1])
    ni, nj = (lines[0][0], lines[0][1]) if it == len(lines) - 1 else (lines[it+1][0], lines[it+1][1])

    if i == pi:
        assert j != pj
        inner_c = i < ni if j < pj else ni < i  # j < pj when going up, else going down
        rng = min(j, pj), max(j, pj)
        boundary_i[i].append(rng)
    else:
        assert j == pj
        inner_c = nj < j if i < pi else j < nj # i < pi when going left, else going right
        rng = min(i, pi), max(i, pi)
        for i_ in range(rng[0]+1, rng[1]):
            boundary_i[i_].append((j, j))
    corners = CORNERS_IN if inner_c else CORNERS_OUT
    corners.add((i, j))

for v in boundary_i.values():
    v.sort()


# Given the boundary information, evaluate the interior, again by column
# and again using ranges, although now ranges represent regions in the
# interior.
inside_i = defaultdict(list)
for i, rngs in boundary_i.items():
    rngs_inside = []
    rngs.reverse()
    inside = False
    frm = rngs[-1][0]
    while rngs:
        rng = rngs.pop()
        if rng[0] != rng[1]:
            # rng is a straight line between two red tiles
            # to evaluate whether we come out of the line on the inside or
            # outside requires considering if that corner is an inner or
            # outer corner (if inner then will enter the interior)
            frm = frm if frm is not None else rng[0]
            rngs_inside.append((frm, rng[1]))
            pc = (i, rng[1])
            if pc in CORNERS_IN:
                inside = False
                frm = None
            else:
                assert pc in CORNERS_OUT
                inside = True
                frm = rng[1] + 1
        else:
            # rng is just one tile, here we're crossing the boundary...
            # ...moving from inside to outside or vice-versa
            if inside:
                rngs_inside.append((frm, rng[1]))
                frm = None
            else:
                frm = rng[0]
            inside = not inside

    # consolidate the ranges that overlap or are immediately adjacent.
    # (NB this goes back to day 5).
    current = rngs_inside[0]
    for rng in rngs_inside[1:]:
        if current[1] == rng[0] or current[1] + 1 == rng[0]:
            current = (current[0], rng[1])
            continue
        if current[1] < rng[0]:
            inside_i[i].append(current)
            current = rng
            continue
        if current[1] > rng[1]:
            continue
        current = (current[0], rng[1])
    inside_i[i].append(current)

# as part 1 but now ignore a rectangle that has an 'up/down' edge that does not fall
# completely within a range that describes the interior for the corresponding column.
max_ = 0
for i_, (i, j) in enumerate(lines[:-1]):
    for i2, j2 in lines[i_+1:]:
        area = (abs(i2 - i) + 1) * (abs(j - j2 + 1))
        if area <= max_:
            continue

        if not any(rng[0] <= j <= rng[1] and rng[0] <= j2 <= rng[1] for rng in inside_i[i]):
            continue
        if not any(rng[0] <= j <= rng[1] and rng[0] <= j2 <= rng[1] for rng in inside_i[i2]):
            continue

        max_ = max_ if max_ > area else area

print(max_)
