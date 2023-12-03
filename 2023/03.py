"""Day 3: Gear Ratios

Either this year is getting pretty complex pretty quickly or (more likely)
I've missed the obvious here and over-complicated it.

part a: 1hr 47mins! Took an age to debug. Unwittingly assumed that
a number wouldn't be repeated on the same line. (I was using .find() to
locate the index of numbers that I'd previously extracted - worked with
the test data 😏.)

part b: 56mins.
total: 163mins, 14x bottom of the leaderboard.
"""

from aocd import get_data

raw = get_data(day=3, year=2023)

lines = raw.splitlines()

# create GRID

GRID = {}
for r, row in enumerate(lines):
    for c, value in enumerate(row):
        GRID[complex(c, r)] = value

VECS = (
    -1j,  # up
    1 - 1j,  # up right
    1,  # right
    1 + 1j,  # down right
    1j,  # down
    -1 + 1j,  # down left
    -1,  # left
    -1 - 1j,  # up left
)

# part a


def adj_to_symb(loc: complex) -> bool:
    """Query if a location is adjacent to a symbol."""
    for vec in VECS:
        adj = loc + vec
        coord = GRID.get(adj, ".")
        if coord != "." and not coord.isdigit():
            return True
    return False


total = 0
for r, row in enumerate(lines):
    val, locs = "", []
    for c, char in enumerate(row):
        if char.isdigit():
            val += char
            locs.append(complex(c, r))

            if c == len(row) - 1:
                # identifed number at end of row
                for loc in locs:
                    if adj_to_symb(loc):
                        total += int(val)
                        break
        elif val:
            # identifed a number
            for loc in locs:
                if adj_to_symb(loc):
                    total += int(val)
                    break
            val, locs = "", []

print(total)

# part b


def adj_star(loc: complex) -> complex:
    for vec in VECS:
        adj = loc + vec
        if GRID.get(adj, "") == "*":
            return adj
    return complex()


def get_number(loc: complex) -> str:
    """Get full number where part of number is at `loc`.

    Returns empty string if loc does not represent part of a number.
    """
    if not ((num := GRID.get(loc, "")).isdigit()):
        return ""
    # look right
    next_right = loc + 1
    while (digit := GRID.get(next_right, "")).isdigit():
        num += digit
        next_right += 1
    # look left
    next_left = loc - 1
    while (digit := GRID.get(next_left, "")).isdigit():
        num = digit + num
        next_left -= 1
    return num


def get_ratio(locs: list[complex]) -> int:
    """Get gear ratio for a number that occupies `locs`."""
    for loc in locs:
        if star := adj_star(loc):
            all_adjs = {star + vec for vec in VECS}
            adjs = all_adjs.difference(set(locs))
            for adj in adjs:
                if val2 := get_number(adj):
                    return int(val) * int(val2)
    return 0


total = 0
for r, row in enumerate(lines):
    val, locs = "", []
    for c, char in enumerate(row):
        if char.isdigit():
            val += char
            locs.append(complex(c, r))

            # at end of row
            if c == len(row) - 1:
                total += get_ratio(locs)

        elif val:
            total += get_ratio(locs)
            val, locs = "", []

# divide by two as otherwise double accounting for every gear ratio
print(total // 2)
