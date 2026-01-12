"""Day 10: Factory

u/tenthmascot showed how day 10 should be done here:
    https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/

...tremendous work which this code reimplements.

#bifurcation  #bitmasks
"""

import functools
import itertools

from aocd import get_data as aocd_get_data


raw = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

# raw = aocd_get_data(day=10, year=2025)

lines_ = raw.splitlines()
lines_ = [line.split() for line in lines_]
lines = [[line[0]] + [line[1:-1]] + [line[-1]] for line in lines_]
indicators: list[int] = []
combos_all: list[dict[int, tuple[int, list[int]]]] = []
counters_all: list[tuple[int]] = []
for line in lines:
    indicator_ = line[0][1:-1]
    indicators.append(int("".join("0" if c == "." else "1" for c in indicator_), 2))
    counters_all.append(tuple(map(int, line[-1][1:-1].split(","))))
    buttons_ = [tuple(map(int, button[1:-1].split(","))) for button in line[1]]
    width = len(indicator_)
    buttons_bitmask_str = [
        "".join("1" if i in button else "0" for i in range(width))
        for button in buttons_
    ]
    buttons = [int(b, 2) for b in buttons_bitmask_str]
    # Evaluate all possible combinations of buttons in which each button is pressed
    # one or zero times. Record as list of 3-tuple where
    #   [0] integer value representing the bitmask of lights that results from pressing
    #       each button of the combination (with lights starting as all off i.e. all 0)
    #   [1] number of buttons in combination (i.e. the 'cost' of pressing this
    #       conbinations of buttons).
    #   [2] list of int representing by how much each counter would be augmented by the
    #       combination, for example if [3, 1, 0, 0, 1] then the first counter would be
    #       be increased by 3, the second by 1, the third and forth would not be
    #       increased and the last counter would be increased by 1.
    combos: list[tuple[int, int, list[int]]] = []
    # include 0 to provide for pressing no buttons in part 2 (and instead simply
    # bifurcating as is)
    for cost in range(width + 1):
        combos_ = itertools.combinations(buttons, cost)
        for combo in combos_:
            bitmask = functools.reduce(lambda a, b: a ^ b, combo, initial=0)
            counts = functools.reduce(
                lambda acc, but: [
                    a + c
                    for a, c in zip(
                        acc, [int(b) for b in f"{but:0{width}b}"], strict=True
                    )
                ],
                combo,
                initial=[0] * width,
            )
            combos.append((bitmask, cost, counts))
    combos_all.append(combos)

# part 1

# recognising that it makes no sense to press the same button twice, the lowest count
# must come from pressing each button either once or zero times...

total = 0
for indicator, combos in zip(indicators, combos_all, strict=True):
    min_ = float("inf")
    for bitmask, cost, _ in combos:
        if indicator ^ bitmask == 0:
            min_ = min(min_, cost)
    total += min_

print(total, "\n")

# part 2


def odd_part_as_bitmask(counters: tuple[int]) -> int:
    return int("".join([str(c % 2) for c in counters]), 2)


total = 0
for i, (combos, counters) in enumerate(zip(combos_all, counters_all, strict=True)):

    @functools.cache
    def get_num_presses(counters: tuple[int]) -> 0:
        if any(c < 0 for c in counters):
            return float("inf")
        if sum(counters) == 0:
            return 0
        odd_part = odd_part_as_bitmask(counters)
        res = float("inf")
        for bitmask, cost, counts in combos:
            if not bitmask ^ odd_part:
                ncounters = [
                    (c - cnt) // 2 for c, cnt in zip(counters, counts, strict=True)
                ]
                res = min(res, cost + (2 * get_num_presses(tuple(ncounters))))
        return res

    ans = get_num_presses(counters)
    print(f"{i}: {ans}")
    total += ans

print(total)
