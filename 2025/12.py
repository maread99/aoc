"""Day 12: Christmas Tree Farm

Christmas spirit restored.

part 1: 103mins
LOTS of thinking before getting down to it and wondering if any could be
rejected on the simple basis that their gross size was too big regardless
of packing - and saw that this was indeed the only check necessary, with
all others way too small to not fit.

NOTE: The solution works for real input only, NOT the example!

part 2:
Took an age to finish off day 10 part 2 before I could get my last star
🙁.

6300 for single star
13950 last star (on later completing 10 part 2)
"""

from dataclasses import dataclass

from aocd import get_data

# raw = """0:
# ###
# ##.
# ##.

# 1:
# ###
# ##.
# .##

# 2:
# .##
# ###
# ##.

# 3:
# ##.
# ###
# ##.

# 4:
# ###
# #..
# ###

# 5:
# ###
# .#.
# ###

# 4x4: 0 0 0 0 2 0
# 12x5: 1 0 1 0 2 2
# 12x5: 1 0 1 0 3 2
# """

raw = get_data(day=12, year=2025)

blocks = raw.split("\n\n")


@dataclass
class Template:
    id: int
    repr_: str
    shape: list[complex]
    shape_neg: list[complex]

    def size(self) -> int:
        return len(self.shape)

    def __repr__(self) -> str:
        return f"{self.id}\n{self.repr_}\n{self.shape}\n{self.shape_neg}\n"


shapes: list[tuple[str, list[complex], list[complex]]] = []
for block in blocks[:-1]:
    lines = block.splitlines()
    id = int(lines[0].removesuffix(":"))
    s = "\n".join(lines[1:])
    shape, shape_neg = [], []
    for j, line in enumerate(lines[1:]):
        for i, c in enumerate(line):
            to = shape if c == "#" else shape_neg
            to.append(complex(i, j))
    shapes.append(Template(id, s, shape, shape_neg))

SHAPES = tuple(shapes)

tasks = []
for line in blocks[-1].splitlines():
    a, b = tuple(line.split(": "))
    wh = tuple(int(v) for v in a.split("x"))
    presents = tuple(map(int, b.split()))
    tasks.append((wh, presents))

total_gross_fit = 0
surplus = []
for i, ((w, h), nums) in enumerate(tasks):
    area = w * h
    total_size = sum(SHAPES[i].size() * n for i, n in enumerate(nums))
    fits_gross = area >= total_size
    total_gross_fit += fits_gross

print(f"{total_gross_fit=}")
