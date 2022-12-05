"""Day 5: Supply Stacks"""

import copy
import re

from aocd import get_data

raw = get_data(day=5, year=2022)

data_stacks, data_moves = raw.split("\n\n")

# Alternative evaluation of `stacks_initial` by transposing data
data_stacks = data_stacks.splitlines()[:-1]
# reduce to letters or spaces
data_stacks_lines: tuple[str] = [line[1::4] for line in data_stacks]
stacks_initial = []
for tup_chars in zip(*data_stacks_lines):
    crates = ''.join(tup_chars).strip()
    stacks_initial.append(list(crates[::-1]))

moves = data_moves.splitlines()
moves = [list(map(int, re.findall(r"\d+", move))) for move in moves]

# part a

stacks = copy.deepcopy(stacks_initial)


def move_crates(num: int, frm: int, to: int):
    for _ in range(num):
        transfer = stacks[frm].pop()
        stacks[to].append(transfer)


for num, frm, to in moves:
    move_crates(num, frm - 1, to - 1)

print("".join([stack[-1] for stack in stacks]))


# part b

stacks = copy.deepcopy(stacks_initial)


def move_crates(num: int, frm: int, to: int):
    transfer, remain = stacks[frm][-num:], stacks[frm][:-num]
    stacks[frm] = remain
    stacks[to].extend(transfer)


for num, frm, to in moves:
    move_crates(num, frm - 1, to - 1)

print("".join([stack[-1] for stack in stacks]))
