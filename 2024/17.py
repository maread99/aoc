"""Day 17: Chronospatial Computer

part a: 2hours 15mins
Excluding pointless debugging, 1hour dead
I spent 50mins coding it, 10mins debugging to find a careless error where
I was using the literal operands instead of the combos in the bdv and cdv
ops, THEN spent a further 1hr 15mins of debugging in which couldn't find
any signs of a bug. (The solution worked for all the examples, I reread the
instructions, double checked any interpretations I wasn't sure on, checked
that the inputs were parsing correctly, even manually walked through the
first few instructions. What else to do?)

Used somebody else's part a solution to get my answer and there it was...
aoc was asking for the string with the values separated by commas, as
indeed shown for the example. I'd read it as / assumed it was asking for 
the value if each output value were joined together "on" the commas to give
a single integer value (since when did AOC take anything other than an
integer for an answer!?). Well over an hour debugging something that
actually worked. I was sufficiently sure it should work that I submitted
the same answer twice. I did think that maybe aoc was after a string answer
to confuse the LLMs and so entered my integer as "123123123", i.e. with the
quotation marks. Didn't pick up that it was after the comma separated
string. Perhaps should have been obvious from how the example answer was
presented, although my thoughts turned to recent puzzles when an answer
hadn't been offered for the example and assumed the same was happening
here, again perhaps in an attempt to confuse the LLMs.

Excuses, excuses. Should have thought more about how aoc was asking for the
answer - which did seem different to normal. Having failed to find a bug,
that's where I should have focused.

part b: 1hour 55mins
I didn't bother trying to reverse engineer the ops, rather saw that there
was a pattern in the A values where the first n digits of the output match
the program. Used this pattern to massively narrow down the values that I
threw into a 'brute force' solve. It solves pretty much immediately.

If I get a chance I may explore an alternative solution that seeks to work
the ops in reverse somehow.

total: 4hrs 10mins, 5.6x bottom of the leaderboard.
(Total would have been 2hours 50mins if take off the time spent with
pointless debugging, 4.0x bottom of the leaderboard.)

#codify-rules  #patterns
"""

from itertools import pairwise, cycle
from aocd import get_data

raw = get_data(day=17, year=2024)

# raw = """Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0
# """

regs, prog_ = raw.split("\n\n")

prog = [int(c) for c in prog_.split(": ")[-1].split(",")]

a, b, c = [int(r.split(" ")[-1]) for r in regs.splitlines()]
lst = [0, 1, 2, 3, a, b, c]
OUT = []

reg_mp = {
    "A": 4,
    "B": 5,
    "C": 6,
}


def adv(v):
    lst[reg_mp["A"]] = lst[reg_mp["A"]] // (2 ** lst[v])


def bxl(v):
    lst[reg_mp["B"]] = lst[reg_mp["B"]] ^ v


def bst(v):
    lst[reg_mp["B"]] = lst[v] % 8


def bxc(_):
    lst[reg_mp["B"]] = lst[reg_mp["B"]] ^ lst[reg_mp["C"]]


def out(v):
    prnt = lst[v] % 8
    OUT.append(prnt)


def bdv(v):
    lst[reg_mp["B"]] = lst[reg_mp["A"]] // (2 ** lst[v])


def cdv(v):
    lst[reg_mp["C"]] = lst[reg_mp["A"]] // (2 ** lst[v])


mp = {
    0: adv,
    1: bxl,
    2: bst,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


# part a

pointer = 0
while pointer < len(prog):
    op, v = prog[pointer : pointer + 2]
    if op == 3:  # jnz
        pointer = v if lst[reg_mp["A"]] else pointer + 2
        continue
    mp[op](v)
    pointer += 2

print(",".join([str(v) for v in OUT]))
# NOT 150174103, rather 1,5,0,1,7,4,1,0,3  !!!!!!!!!!!!


# part b
def find_pattern(vals: list) -> list:
    """find the longest repeating pattern in `vals`."""
    for lgn in reversed(range(1, len(vals) // 2)):
        n = 1
        while lgn * (n + 1) < len(vals):
            if vals[:lgn] != vals[lgn * n : lgn * (n + 1)]:
                break
            n += 1
        else:
            # verify that any 'part' at the end also matches...
            vals_end = vals[-(len(vals) % lgn * (n + 2)) :]
            if vals_end == vals[: len(vals_end)]:
                return vals[:lgn]
    return []


i = 0
diffs = [1]
itr = cycle(diffs)

digit_n = 1
matches = []
# a pattern emerges in the A values that match at least the first n digits
# of the output with the program, where 1 <= n <= len(prog). The pattern
# lies in the differences between a value that matches at least n digits
# and the next lowest value that also matches at least n digits. Uncomment
# the print line to print the pattern for n = 4 (mine was 68 differences
# long. I suspect the same pattern comes out for everyone).
while True:
    i += next(itr)
    lst = [0, 1, 2, 3, i, b, c]
    outi = 0
    OUT = []
    pointer = 0
    while pointer < len(prog):
        op, v = prog[pointer : pointer + 2]
        if op == 3:  # jnz
            pointer = v if lst[reg_mp["A"]] else pointer + 2
            continue
        mp[op](v)
        if op == 5:
            if OUT[outi] != prog[outi]:  # not matching
                break
            if len(OUT) == len(prog):
                print(i)
                exit()
            outi += 1
        pointer += 2

    if len(OUT) > digit_n:
        matches.append(i)  # first n digits of output match program, so add it

    # if have a decent number of matches then look for a pattern...
    if len(matches) > (300 // digit_n) and not len(matches) % 50:
        diffs = [b - a for a, b in pairwise(matches)]
        if not (ptn := find_pattern(diffs)):
            continue  # wait another 50 or so matches before looking again

        # have found a pattern that locks in another digit, go with this new pattern
        itr = cycle(ptn)

        # if digit_n == 4:
        #     print("Ptn for n = 4:", ptn)

        # and now look for a pattern that matches the next digit as well...
        digit_n += 1
        # ...setting off from largest value of A checked that fitted the prior pattern
        i = matches[-(len(matches) % len(ptn))]
        matches = []
