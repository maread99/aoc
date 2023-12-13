"""Day 12: Hot Springs

part a: 1hr 36mins
The actual brute force implementation that I got part a out with is
`12_alt.py`. Offered nowhere near the necessary performance for part b.

part b: >8hrs
Took an age to get it out. Some optimization of the brute force approach
provided for getting out most of the lines, but it was never going to able
to solve the more demanding lines.

Tried rewritting part a as a DFS rather than recursion and realised that I
was just doing the same thing in a different way.

Breaking it down block by block brought about a major performance
enhancement, allowing for getting out more lines, but still not all.

Spent some time considering if using regexs would be an option, and
explored writing part a on that basis, thinking that underneath there would
be an efficient algorithm. Abandoned.

Only needed a peak at others' solutions to see that recursion or DFS
approach is the way to go but that I'd neglected to USE A CACHE!!!

Next day with a clearer head rewrote this recursive approach, including a
cache. (Ended up using the original `12_alt.py` to debug it.)

(Any references to ships or boats in the comments relates to thinking in
terms of placing boats, as in a context of battleships.)

For reference, the exemplar solution again goes to hyper-neutrino...have a
look and weep:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2023/day12p2.py
(It could even use be changed to use the `functools.cache` decorator to
save a further 6 lines of code!)

#recursion  #memoization
"""

import functools
from aocd import get_data

raw = get_data(day=12, year=2023)

# raw = """???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# """


@functools.cache
def block_leftovers(block: str, v: int) -> list[str]:
    """List of all possible leftovers.

    A leftover is what's left of the block to the right of where the ship's
    placed, including provision for 1 space margin. Will be an empty str
    if no part of the block remain.
    """
    leftovers: list[str] = []
    for i in range(len(block)):
        # end represents right end of boat
        end = i + v - 1
        if end == len(block):
            break
        if end < len(block) - 1 and block[end + 1] == "#":
            continue  # right would butt against #
        # start represents left end of boat
        start = i
        if "#" in block[:start]:
            break  # should have consumed it

        leftovers.append(block[end + 2 :])
    return leftovers


@functools.cache
def count_options(path: str, values: tuple[int, ...]) -> int:
    path = path.strip(".")

    if not values:
        if not path or "#" not in path:
            return 1
        return 0

    if len(path) < sum(values):
        return 0  # not enough room left to fit the remaining ships

    if "." in path:
        block, path = path.split(".", maxsplit=1)
    else:
        block = path
        path = ""

    v = values[0]

    options = []
    if "#" not in block:
        options.append((path, values))  # option to not consume any ship

    if len(block) < v:
        if "#" in block:
            return 0  # has to consume a ship but can't
    elif len(block) == v:
        options.append((path, values[1:]))  # fully consumes ship
    else:
        leftovers = block_leftovers(block, v)
        if not leftovers:  # not consumed
            if "#" in block:
                return 0
        else:
            for leftover in block_leftovers(block, v):
                options.append((leftover + "." + path, values[1:]))
    sum_to = sum((count_options(*opts) for opts in options))  # TODO TIDY
    return sum_to


# part a


def get_path_values(line: str) -> tuple[str, tuple[int, ...]]:
    path, values = line.split()
    return path, tuple(map(int, values.split(",")))


total = 0
for n, line in enumerate(raw.splitlines()):
    path, values = get_path_values(line)
    total += count_options(path, values)

print(total)


# part b


def unfold(line: str) -> tuple[str, tuple[int, ...]]:
    full_path_, values_ = line.split()
    full_path = "?".join([full_path_] * 5)
    values = ",".join([values_] * 5)
    return full_path, tuple(map(int, values.split(",")))


total = 0
for n, line in enumerate(raw.splitlines()):
    path, values = unfold(line)
    total += count_options(path, values)

print(total)
