"""Day 17: Pyroclastic Flow.

part a, 150mins, too much of which was debugging as a result of not
initially comprehending aspects of the dynamics, including:
    Didn't appreciate jet blast and drop have to be implemented separately
    in order to have accessible the rock position prior to hitting
    something solid.

    Didn't consider that could jet blast sideways into solid.

    Didn't appreciate that the data repeats when exhuasted!

    Didn't account for the fact that the highest point of a new rock could
    be lower than the highest point of all previous rocks.

part b, 120mins, including reading through a stackoverflow reply on how to
find patterns in a sequence.
"""

from collections.abc import Callable
import itertools

from aocd import get_data


raw = get_data(day=17, year=2022)

ROCKS = (
    (2, 3, 4, 5),
    (3, 2 + 1j, 3 + 1j, 4 + 1j, 3 + 2j),
    (2, 3, 4, 4 + 1j, 4 + 2j),
    (2, 2 + 1j, 2 + 2j, 2 + 3j),
    (2, 3, 2 + 1j, 3 + 1j),
)


def get_rock(i: int, y: int):
    """Get next rock.

    y: int
        y level of current highest solid
    """
    template = ROCKS[i % 5]
    y_ = complex(0, y + 4)
    return [c + y_ for c in template]


def simulate(
    n: int, break_cond: Callable = lambda _, __: False
) -> tuple[int, list[int], int]:
    jet = itertools.cycle(raw)
    solid = set(range(7))
    dy: list[int] = []  # NOTE dy is not required for part a
    y = 0

    def blast(r: list[complex]) -> list[complex]:
        j = next(jet)
        if j == "<":
            nr = [c - 1 for c in r]
            if any(c.real == -1 for c in nr):
                return r
        else:
            nr = [c + 1 for c in r]
            if any(c.real == 7 for c in nr):
                return r
        return r if any(c in solid for c in nr) else nr

    def drop(r: list[complex]) -> list[complex]:
        return [c - 1j for c in r]

    for i in range(n):
        if break_cond(i, dy):
            return (y, dy, i)
        nr = get_rock(i, y)
        for _ in range(4):
            r = blast(nr)
            nr = drop(r)

        while not any(c in solid for c in nr[:4]):
            # NOTE could probably be further optimised to only check those cells along
            # the leading edge of those rocks with a leading edge narrower than 4 cells.
            r = blast(nr)
            nr = drop(r)

        yp = y
        y = max(y, int(max(c.imag for c in r)))
        dy.append(y - yp)
        solid |= set(r)

    return y, dy, i


print(simulate(2022)[0])

# part b
# both inputs, rocks and blasts, are recurring. Reasonable to expect that this will
# result in a pattern emerging at some point. For ease of calculating part b, looked for
# pattern in the change in height. Suspect how often the pattern repeats is determined
# by how both inputs (jet and rock) synchronise over time. I just looked for a pattern
# in a large sample (originally 1_000_000 rocks, 15s to run).
SAMPLE_LENGTH = 100_000
y, dy, _ = simulate(SAMPLE_LENGTH)

# Working back from end of sample, look for a pattern that matches consistently
# throughout the sample.
for i in range(1, SAMPLE_LENGTH // 2):
    pattern = dy[-i:]
    if all(pattern == dy[-i * j : -i * (j - 1)] for j in range(2, SAMPLE_LENGTH // i)):
        break
ptrn_len = len(pattern)

# evaluate when first occurrence of pattern completes

break_cond = lambda i, dy: i >= ptrn_len and dy[-ptrn_len:] == pattern
y, dy, n = simulate(ptrn_len * 2, break_cond)

h_start = y  # height through to end of first pattern
N = 1000000000000 - n  # number of rocks left to fall
h_mid = sum(pattern) * (N // ptrn_len)  # height added during remaining full patterns
h_end = sum(pattern[: N % ptrn_len])  # height added from end of h_mid to last rock
print((h_start + h_mid + h_end))
