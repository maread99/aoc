"""Day 13: Point of Incidence

This is NOT a good solution. See 13_rev.py for a very much less complicated
way to do this.

part a: 120mins
Very much overcomplicated it.

part b: 90mins.
Started on the wrong foot by assuming that the previous mirror would no
longer remain intact.

total: 3hrs 30mins, 15x bottom of the leaderboard.

#arrays
"""

from aocd import get_data

raw = get_data(day=13, year=2023)

# raw = """#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#
# """

pats = raw.split("\n\n")


def get_pat_value(
    rows: list[list[str]] | list[str],
    invalid_col_syms: tuple[tuple[int, int], tuple[int, int]] | None = None,
    invalid_row_syms: tuple[tuple[int, int], tuple[int, int]] | None = None,
):
    cols = [col for [*col] in zip(*rows)]
    LEN_COLS = len(cols)

    # look for mirror that fully reflects left hand side
    col_sym_lhs = (0, 0)
    for i in range(1, (LEN_COLS // 2) + 1):
        refl_width = i
        lhs = cols[:i]
        rhs = cols[i : i + refl_width][::-1]
        if lhs == rhs:
            col_sym_lhs_ = (refl_width, i)
            if invalid_col_syms is not None and col_sym_lhs_ == invalid_col_syms[0]:
                continue
            col_sym_lhs = col_sym_lhs_
            break

    # look for mirror that fully reflects right hand side
    col_sym_rhs = (0, 0)
    for i in range(LEN_COLS // 2, LEN_COLS):
        refl_width = LEN_COLS - i - 1
        lhs = cols[i + 1 :]
        rhs = cols[i - refl_width + 1 : i + 1][::-1]
        if lhs == rhs:
            col_sym_rhs_ = (refl_width, i + 1)
            if invalid_col_syms is not None and col_sym_rhs_ == invalid_col_syms[1]:
                continue
            col_sym_rhs = col_sym_rhs_
            break

    assert not col_sym_lhs[0] or not col_sym_rhs[0]

    # look for mirror that fully reflects upper side
    LEN_ROWS = len(rows)
    row_sym_up = (0, 0)
    for i in range(1, (LEN_ROWS // 2) + 1):
        refl_width = i
        lhs = rows[:i]
        rhs = rows[i : i + refl_width][::-1]
        if lhs == rhs:
            row_sym_up_ = (refl_width, i)
            if invalid_row_syms is not None and row_sym_up_ == invalid_row_syms[0]:
                continue
            row_sym_up = row_sym_up_
            break

    # look for mirror that fully reflects lower side
    row_sym_down = (0, 0)
    for i in range(LEN_ROWS // 2, LEN_ROWS):
        refl_width = LEN_ROWS - i - 1
        lhs = rows[i + 1 :]
        rhs = rows[i - refl_width + 1 : i + 1][::-1]
        if lhs == rhs:
            row_sym_down_ = (refl_width, i + 1)
            if invalid_row_syms is not None and row_sym_down_ == invalid_row_syms[1]:
                continue
            row_sym_down = row_sym_down_
            break

    assert not row_sym_up[0] or not row_sym_down[0]

    col_sym = max((col_sym_lhs, col_sym_rhs))
    row_sym = max((row_sym_up, row_sym_down))

    assert col_sym[0] or row_sym[0]
    assert col_sym[0] != row_sym[0]
    if col_sym[0] > row_sym[0]:
        res = col_sym[1]
    else:
        res = row_sym[1] * 100
    return res, (col_sym_lhs, col_sym_rhs), (row_sym_up, row_sym_down)


# part a

a_results = []
total = 0
for pat in pats:
    rows = pat.splitlines()
    res = get_pat_value(rows)
    a_results.append(res)
    total += res[0]

print(total)

# part b

total = 0
for n, pat in enumerate(pats):
    rows = pat.splitlines()
    rows = [list(row) for row in rows]
    prev_total = total
    a_res = a_results[n]
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            c_prev = c
            row[i] = "#" if c == "." else "."
            try:
                v, *rest = get_pat_value(rows, a_res[1], a_res[2])
            except AssertionError:
                pass
            else:
                total += v
            finally:
                row[i] = c_prev
            if total != prev_total:
                break
        if total != prev_total:
            break
    else:
        assert False

print(total)
