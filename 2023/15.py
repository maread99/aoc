"""Day 15: Lens Library

Seems like an elf stuck a 5 on the end of the day 1 puzzle.

part a: 6mins
part b: 29min
Spent more time trying to understand the question than implementing the
solution.

No bugs! 🥳

total: 35mins, 3.2x bottom of the leaderboard.

#mappings
"""

from collections import defaultdict

from aocd import get_data

raw = get_data(day=15, year=2023)

# raw = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

parts = raw.split(",")


def get_hash(label: str) -> int:
    v = 0
    for c in label:
        v += ord(c)
        v *= 17
        v %= 256
    return v


# part a

total = 0
for part in parts:
    total += get_hash(part)

print(total)


# part b


def get_step_info(part: str) -> tuple[str, int, bool, int]:
    """Get label, hash, if insert as bool, focal length."""
    split_on = "=" if "=" in part else "-"
    lab, _ = part.split(split_on)
    hash_ = get_hash(lab)
    if split_on == "=":
        return lab, hash_, True, int(part[-1])
    return lab, hash_, False, 0


BOXES: dict[int, dict[str, int]] = defaultdict(dict)

for part in parts:
    label, hsh, insert, fl = get_step_info(part)
    if insert:
        BOXES[hsh][label] = fl
    else:
        BOXES[hsh].pop(label, "")

fp = 0
for box_num, box in BOXES.items():
    for i, (label, fl) in enumerate(box.items()):
        fp += (box_num + 1) * (i + 1) * fl

print(fp)
