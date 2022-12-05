"""Day 5: Supply Stacks"""

import copy
import re

from aocd import get_data

raw = get_data(day=5, year=2022)

data_stacks, data_moves = raw.split("\n\n")

stacks_initial = [[] for _ in range(9)]

for line in reversed(data_stacks.splitlines()[:-1]):
    for i in range(9):
        start = (i * 4) + 1
        crate = line[start : start + 1]
        if crate.strip():
            stacks_initial[i].append(crate)

    # better...
    # for i, crate in enumerate(line[1::4]):
    #     if crate.strip():
    #         stacks_initial[i].append(crate)

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
