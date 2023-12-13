"""Day 12: Hot Springs

NOTE NOTE NOTE Part a ONLY. Solution here does NOT work for real input for
part b! (See `12.py` for a better solution.)

Initial half-baked brute force recursive solution that tries every possible
combination and counts those that are valid.

#recursion
"""

from aocd import get_data

raw = get_data(day=12, year=2023)

raw = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def valid(path: str, values: list[int], final: bool = False) -> bool:
    blocks = [block for block in path.split(".") if block]
    if len(blocks) > len(values):
        return False
    if final and len(blocks) != len(values):
        return False
    if not blocks:
        return True

    for block, v in zip(blocks[:-1], values):
        if len(block) != v:
            return False
    if len(blocks[-1]) > values[len(blocks) - 1]:
        return False
    if final and len(blocks[-1]) != values[-1]:
        return False
    return True


def count_options_for_line(fullpath: str, values: list[int]):
    def count_options(path: str = "") -> int:
        final = len(path) == len(fullpath)
        if not valid(path, values, final):
            return 0
        if final:
            return 1
        start = len(path)
        for n in fullpath[start:]:
            if n == "?":
                break
            if n == ".":
                path += n
                continue
            else:
                return count_options(path + n)
        if len(path) == len(fullpath):
            if valid(path, values, True):
                return 1
            return 0
        return count_options(path + ".") + count_options(path + "#")

    return count_options()


lines = raw.splitlines()

# part a


def get_path_values(line: str) -> tuple[str, list[int]]:
    path, values = line.split()
    return path, list(map(int, values.split(",")))


total = 0
for line in lines:
    fullpath, values = get_path_values(line)
    v = count_options_for_line(fullpath, values)
    total += v
print(total)


# part b
# NOTE NOTE NOTE WORKS WITH EXAMPLE ONLY, will not solve real input in a hurry!


def unfold(line: str) -> tuple[str, list[int]]:
    full_path_, values_ = line.split()
    full_path = "?".join([full_path_] * 5)
    values = ",".join([values_] * 5)
    return full_path, list(map(int, values.split(",")))


total = 0
for n, line in enumerate(lines):
    fullpath, values = unfold(line)
    v = count_options_for_line(fullpath, values)
    total += v
print(total)
