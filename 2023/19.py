"""Day 19: Aplenty

part a: 1hr 50mins
Ran into problems. Can't believe I didn't know (or at least forgot) that if
within a loop you define a lambda or function that refers to a variable
defined inside the loop then the value of that variable assumed in every
defined lambda will be the variable's value as defined in the last
iteration of the loop, NOT the variable's value at the time the lambda was
defined.

part b: 3hr 45mins
Had a bug in the negative case structural pattern matching. Not quite sure
how I took this long as I got the core of the implementation out relatively
quickly. When the example answer didn't come out I think I lost faith in
it rather than look harder for the bug. Only came back to it later.

total: 5hr 35mins, 11.5x bottom of the leaderboard.

#recursion
"""

import copy
import math
import re
from collections import defaultdict

from aocd import get_data

raw = get_data(day=19, year=2023)

# raw = """px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}

# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}
# """

lines, parts = raw.split("\n\n")


RULES: dict[str, list[tuple[str, ...]]] = defaultdict(list)

for line in lines.splitlines():
    name, rest = line.split("{")
    rules = rest[:-1].split(",")
    for rule in rules:
        RULES[name].append(tuple(rule.split(":")))


# part a


def call_rule(name, values: tuple[int]) -> int:
    x, m, a, s = values  # referred to by the eval statement
    for rule in RULES[name]:
        if len(rule) > 1:
            expr, rtrn = rule
            if not eval(expr):
                continue
        else:
            rtrn = rule[0]

        if rtrn == "A":
            return sum(values)
        if rtrn == "R":
            return 0
        return call_rule(rtrn, values)
    assert False


total = 0
for part in parts.splitlines():
    values = tuple(map(int, re.findall(r"\d+", part)))
    total += call_rule("in", values)

print(total)


# part b

total = 0


def call_b(
    rule: tuple[str, str] | tuple[str],
    values: tuple[list[int]],
    neg_cases: tuple[tuple[str, ...] | tuple[str, str]],
):
    global total

    if len(rule) == 1:
        rule_ = rule[0]
        if rule_ == "A":
            total += math.prod(b - a + 1 for a, b in values)
            return
        if rule_ == "R":
            return
        return call_b(RULES[rule_][0], values, RULES[rule_][1:])

    xx, mm, aa, ss = values
    xx_, mm_, aa_, ss_ = copy.deepcopy(values)

    expr, rtrn = rule
    cat, symb = expr[0], expr[1]
    v = int(expr[2:])

    # positive case
    match cat, symb:
        case "x", ">":
            xx_[0] = max(xx_[0], v + 1)
        case "x", "<":
            xx_[1] = min(xx_[1], v - 1)
        case "m", ">":
            mm_[0] = max(mm_[0], v + 1)
        case "m", "<":
            mm_[1] = min(mm_[1], v - 1)
        case "a", ">":
            aa_[0] = max(aa_[0], v + 1)
        case "a", "<":
            aa_[1] = min(aa_[1], v - 1)
        case "s", ">":
            ss_[0] = max(ss_[0], v + 1)
        case "s", "<":
            ss_[1] = min(ss_[1], v - 1)

    call_b(tuple([rtrn]), [xx_, mm_, aa_, ss_], [])

    # negative case
    match cat, symb:
        case "x", ">":
            # initial bug: xx[1] = max(xx[1], v)  # !!!
            xx[1] = min(xx[1], v)
        case "x", "<":
            xx[0] = max(xx[0], v)
        case "m", ">":
            mm[1] = min(mm[1], v)
        case "m", "<":
            mm[0] = max(mm[0], v)
        case "a", ">":
            aa[1] = min(aa[1], v)
        case "a", "<":
            aa[0] = max(aa[0], v)
        case "s", ">":
            ss[1] = min(ss[1], v)
        case "s", "<":
            ss[0] = max(ss[0], v)

    call_b(neg_cases[0], [xx, mm, aa, ss], neg_cases[1:])


call_b(
    RULES["in"][0],
    [[1, 4000], [1, 4000], [1, 4000], [1, 4000]],
    RULES["in"][1:],
)

print(total)
