"""Day 19: Not Enough Minerals

Adds further optimisations as picked up by a full read-through of:
    https://github.com/mebeim/aoc/tree/master/2022#day-19---not-enough-minerals

I've marked it as an alternate version rather than revised as implementing
these would have taken me longer than the execution time saved.

part a was 50s, with further optimisations here now 23s
part b was 110s, with further optimisations here now 29s

There are almost certainly further optimisations that haven't been included
here.
"""

import math
import re

from aocd import get_data

raw = get_data(day=19, year=2022)
lines = raw.splitlines()


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", s)))


def max_poss(g: int, gr: int, tm: int) -> int:
    """Return maximum possible geodes given time remaining."""
    existing = g + (gr * tm)
    tm -= 1
    new = (tm * tm) - sum(range(1, tm))
    return new + existing


def solve_line(line: str, start_tm: int, quality: bool = True):
    bp, ore_ore, clay_ore, obs_ore, obs_clay, geode_ore, geode_obs = ints(line)
    COSTS = [(geode_ore, geode_obs), (obs_ore, obs_clay), (clay_ore, 0), (ore_ore, 0)]
    MAX_REQ = [float("inf"), COSTS[0][1], COSTS[1][1], max(cost[0] for cost in COSTS)]

    # time, robots * 4, stuff * 4; geode, obs, clay, ore
    stack = [(start_tm, 0, 0, 0, 1, 0, 0, 0, 0, [])]
    max_ = 0
    seen = set()

    while stack:
        state_ = stack.pop()
        state = state_[:-1]
        wait_build = state_[-1]
        if state in seen:
            continue
        seen.add(state)
        tm, robots, stuff = state[0], list(state[1:5]), list(state[5:])

        if not tm:
            max_ = max(max_, stuff[0])
            continue

        if max_poss(stuff[0], robots[0], tm) < max_:
            continue

        tm -= 1

        build = [0, 0, 0, 0]
        for i, (c_ore, c_other) in enumerate(COSTS):
            if robots[i] == MAX_REQ[i]:
                continue
            if c_ore <= stuff[-1] and (i == 3 or c_other <= stuff[i + 1]):
                if wait_build and wait_build[i]:
                    # if could have built it last time and didn't then
                    # suboptimal to build it now
                    continue
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
                stack.append((tm, *robots_, *stuff_, []))
                if not i:
                    break  # if can build a geode robot then build it, no more questions

        if not build[0] and any(
            not build[i] and robots[i] != MAX_REQ[i] for i in range(1, 4)
        ):
            # add option to wait only if not building a geode robot and
            # can't build every other robot type that could need
            stack.append((tm, *robots, *stuff, build))

    return max_ * (bp if quality else 1)


print(sum(solve_line(line, 24) for line in lines))

print(math.prod(solve_line(line, 32, False) for line in lines[:3]))
