"""Day 6: Tuning Trouble"""

from aocd import get_data

data = get_data(day=6, year=2022)


def length_to_marker(data: str, num_unique: int) -> int:
    """Return length of start of `data` to marker.

    Returns length of `data` preceeding marker where marker immediately
    follows the first occurence in `data` of `num_unique` unique
    characters.

    Return is equivalent to marker position.
    """
    n = num_unique
    for i in range(len(data)):
        if len(set(data[i : i + n])) == n:
            break
    return i + n


print(length_to_marker(data, 4))
print(length_to_marker(data, 14))
