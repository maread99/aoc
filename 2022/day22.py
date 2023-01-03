"""Day 22: Monkey Map.

part a 110mins, over half an hour looking for a bug which was wrapping to
the wrong end when changing row. Should have picked up the bug on
inspection without having to walkthrough the example.

part b, many hours, considered trying to write a global solution which
would work for any input, perhaps using matrix transformations to track the
folds and then evaluate the touching edges, or evaluating all adjoining
edges given those which are known (got so far as evaluating the vertices of
each folded face altough it seemed to much of a leap from there to pairing
edges of faces in each direction).

Ended up with a solution which hard-codes wrapping mappings from inspection
of the raw data.
"""

from collections import defaultdict, deque

from aocd import get_data


raw = get_data(day=22, year=2022)


lines = raw.splitlines()

MOVES = lines[-1]

# create board and assertain bounds of each row / column
BOARD = {}
START = None
ROW_BOUNDS = defaultdict(list)
COL_BOUNDS = defaultdict(list)

for j, line in enumerate(lines[:-2], start=1):
    for i, char in enumerate(line, start=1):
        if not char.strip():
            continue
        if START is None:
            START = complex(i, j)
        if j not in ROW_BOUNDS:
            ROW_BOUNDS[j].append(i)
        if i not in COL_BOUNDS:
            COL_BOUNDS[i].append(j)
            COL_BOUNDS[i].append(j)
        COL_BOUNDS[i][1] = j
        key = complex(i, j)
        BOARD[key] = 1 if char == "." else 0
    ROW_BOUNDS[j].append(i)


move = iter(MOVES)
directions = deque([1, 1j, -1, -1j])
pos = START

break_ = False
while True:
    next_move = next(move)
    num: str | int = ""
    while next_move.isdigit():
        num += next_move
        try:
            next_move = next(move)
        except StopIteration:
            break_ = True
            break

    num = int(num)
    turn = next_move
    direction = directions[0]
    for _ in range(num):
        npos = pos + direction
        if npos not in BOARD:
            # wrap
            if direction == 1:
                npos = complex(ROW_BOUNDS[pos.imag][0], pos.imag)
            if direction == -1:
                npos = complex(ROW_BOUNDS[pos.imag][1], pos.imag)
            if direction == -1j:
                npos = complex(pos.real, COL_BOUNDS[pos.real][1])
            if direction == 1j:
                npos = complex(pos.real, COL_BOUNDS[pos.real][0])
        if not BOARD[npos]:  # i.e. if wall
            break
        pos = npos

    if break_:
        break

    directions.rotate(1 if turn == "L" else -1)

FACING_MAPPING = {1: 0, 1j: 1, -1: 2, -1j: 3}
print(int((pos.imag * 1000) + (pos.real * 4) + FACING_MAPPING[direction]))

# part b

# evaluate each cube face as its four indices as on the 2D board
FACES = []
for y_, line in enumerate(lines[:-2][::50]):
    for x_, char in enumerate(line[::50]):
        if char.strip():
            x, y = 1 + x_ * 50, 1 + y_ * 50
            FACES.append(
                [
                    complex(x, y),
                    complex(x + 49, y),
                    complex(x, y + 49),
                    complex(x + 49, y + 49),
                ]
            )

BOUNDS_INDICES = {
    -1j: (0, 1),
    1: (1, 3),
    1j: (2, 3),
    -1: (0, 2),
}


def get_edge_coords(face: int, edge: complex, reverse: bool = False) -> list[complex]:
    """Get the board coordinates for a given edge of a given face."""
    VERTICES = FACES[face]
    frm, to = BOUNDS_INDICES[edge]
    start, end = VERTICES[frm], VERTICES[to]
    if start.real == end.real:
        coords = [
            complex(start.real, j) for j in range(int(start.imag), int(end.imag) + 1)
        ]
    else:
        coords = [
            complex(i, end.imag) for i in range(int(start.real), int(end.real) + 1)
        ]
    if reverse:
        coords.reverse()
    return coords


def get_wrap_mapping(
    a: tuple, b: tuple
) -> dict[tuple[complex, complex], tuple[complex, complex]]:
    """Get wrap mapping, keys and values as 2-tuple defining coord and direction.

    `a` and `b` as tuple of arguments for `get_edge_coords` to define
    coordinates to map.
    """
    keys = get_edge_coords(*a)
    values = get_edge_coords(*b)
    mapping = {(k, a[1]): (v, -b[1]) for k, v in zip(keys, values)}
    rvrsd = {(v, b[1]): (k, -a[1]) for k, v in zip(keys, values)}
    return mapping | rvrsd


# THESE WRAPS REQUIRE HARD-CODING FROM INSPECTION OF THE RAW DATA
WRAP05 = get_wrap_mapping((0, -1j), (5, -1))
WRAP03 = get_wrap_mapping((0, -1), (3, -1, True))
WRAP15 = get_wrap_mapping((1, -1j), (5, 1j))
WRAP14 = get_wrap_mapping((1, 1), (4, 1, True))
WRAP12 = get_wrap_mapping((1, 1j), (2, 1))
WRAP23 = get_wrap_mapping((2, -1), (3, -1j))
WRAP45 = get_wrap_mapping((4, 1j), (5, 1))
WRAPS = WRAP05 | WRAP03 | WRAP15 | WRAP14 | WRAP12 | WRAP23 | WRAP45

# as for part a with revised wrapping...
move = iter(MOVES)
directions = deque([1, 1j, -1, -1j])
pos = START

break_ = False
while True:
    next_move = next(move)
    num = ""
    while next_move.isdigit():
        num += next_move
        try:
            next_move = next(move)
        except StopIteration:
            break_ = True
            break

    num = int(num)
    turn = next_move
    direction = directions[0]
    for _ in range(num):
        npos = pos + direction
        if npos not in BOARD:
            # wrap
            npos, ndirection = WRAPS[(pos, direction)]
            if BOARD[npos]:
                # not wrapping to a wall, so change direction
                while directions[0] != ndirection:
                    directions.rotate(1)
                direction = directions[0]
        if not BOARD[npos]:  # i.e. if wall
            break
        pos = npos

    if break_:
        break

    directions.rotate(1 if turn == "L" else -1)

print(int((pos.imag * 1000) + (pos.real * 4) + FACING_MAPPING[direction]))
