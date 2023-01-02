"""Day 19: Not Enough Minerals

Didn't get part a out without having to look elsewhere. I had a depth first
search solution which would have taken an eternity to compute. The
walk-through by @mebeim showed that I was on the right track although
lacked optimisations to cut down the search space:
    https://github.com/mebeim/aoc/tree/master/2022#day-19---not-enough-minerals

In particular saw how could never require more of any robot type than the
maximum amount of the corresponding material that could be required to
construct a robot.

Separately, figured that could limit the circumstances in which include an
option to 'wait'.

It's clearly nowhere near optimal, but gets part a out locally in 50s and
part b in 110s.
"""

import math
import re

from aocd import get_data

raw = get_data(day=19, year=2022)
lines = raw.splitlines()


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", s)))


def solve_line(line: str, start_tm: int, quality: bool = True):
    bp, ore_ore, clay_ore, obs_ore, obs_clay, geode_ore, geode_obs = ints(line)
    COSTS = [(geode_ore, geode_obs), (obs_ore, obs_clay), (clay_ore, 0), (ore_ore, 0)]
    MAX_REQ = [float("inf"), COSTS[0][1], COSTS[1][1], max(cost[0] for cost in COSTS)]

    # time, robots * 4, stuff * 4; geode, obs, clay, ore
    stack = [(start_tm, 0, 0, 0, 1, 0, 0, 0, 0)]
    max_ = 0
    seen = set()

    while stack:
        state = stack.pop()
        if state in seen:
            continue
        seen.add(state)
        tm, robots, stuff = state[0], list(state[1:5]), list(state[5:])

        if not tm:
            max_ = max(max_, stuff[0])
            continue

        tm -= 1

        build = [0, 0, 0, 0]
        for i, (c_ore, c_other) in enumerate(COSTS):
            if robots[i] == MAX_REQ[i]:
                continue
            if c_ore <= stuff[-1] and (i == 3 or c_other <= stuff[i + 1]):
                # mark as option to build if have sufficient resources
                build[i] += 1

        # collect
        for i, r in enumerate(robots):
            stuff[i] += r

        for i, build_it in enumerate(build):
            if build_it:
                robots_ = robots.copy()
                robots_[i] += 1
                stuff_ = stuff.copy()
                stuff_[-1] -= COSTS[i][0]
                if i != 3:
                    stuff_[i + 1] -= COSTS[i][1]
                stack.append((tm, *robots_, *stuff_))
                if not i:
                    break  # if can build a geode robot then build it, no more questions

        if not build[0] and any(
            not build[i] and robots[i] != MAX_REQ[i] for i in range(1, 4)
        ):
            # add option to wait only if not building a geode robot and
            # can't build every other robot type that could need
            stack.append((tm, *robots, *stuff))

    return max_ * (bp if quality else 1)


print(sum(solve_line(line, 24) for line in lines))

print(math.prod(solve_line(line, 32, False) for line in lines[:3]))
