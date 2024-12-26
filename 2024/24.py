"""Day 24: Crossed wires

part a: 39mins

part b: 4hours
I'm not sure how long this one took me. Spent a few hours trying a brute
force approach that was going nowhere. Next day looked at it afresh, mapped
out some nodes on paper and realised that it was a pretty simple algo for
binary addition. Interrogated where the errors were. NOTE This solution
will only work if the nature of the errors in the logic are the same for
other puzzle inputs (suspect they are...).

total: 5hours or so, say, 5x bottom of the leaderboard.
"""

import operator
from collections import deque

from aocd import get_data


raw = get_data(day=24, year=2024)

# raw = """x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1

# ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj
# """

# raw = """x00: 1
# x01: 1
# x02: 1
# y00: 0
# y01: 1
# y02: 0

# x00 AND y00 -> z00
# x01 XOR y01 -> z01
# x02 OR y02 -> z02
# """

gates_, conns_ = raw.split("\n\n")

GATES = {}
for g in gates_.splitlines():
    k, v = g.split(": ")
    GATES[k] = bool(int(v))

INSTR = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}

CONNS = []
for c in conns_.splitlines():
    a, op, b, _, out = c.split(" ")
    CONNS.append([a, INSTR[op], b, out])


conns = deque(CONNS.copy())
gates = GATES.copy()
while conns:
    conn = conns.popleft()
    a, op, b, out = conn
    if a not in gates or b not in gates:
        conns.append(conn)
        continue
    gates[out] = op(gates[a], gates[b])

bits = []
for i in range(len(CONNS)):
    k = "z" + ("0" if i < 10 else "") + str(i)
    if k not in gates:
        break
    bits.append(int(gates[k]))

print(int("".join(str(b) for b in reversed(bits)), 2))

# part b

XY = ["x", "y"]

# get gates that perform an xor op on x and y inputs
xy_xors = [
    c for c in CONNS if c[0][0] not in XY and c[2][0] not in XY and c[1] == INSTR["XOR"]
]
# these gates should output to a z output, if this isn't the case then needs swapping
xy_xors.sort(key=lambda x: x[-1])
swaps = [c[-1] for c in xy_xors if c[-1][0] != "z"]

# evaluate z outputs with which the above should be swapped and add to swaps
pn = 0
zs = []
for c in xy_xors:
    if c[-1][0] != "z":
        continue
    n = int(c[-1][1:])
    if n != pn + 1:
        zs.append(pn + 1)
    pn = n

swaps += ["z" + ("0" if z < 10 else "") + str(z) for z in zs]

# identify x, y inputs where the outputs to the AND and XOR gates needs swapping
for c in CONNS:
    if c[0][0] in XY and c[2][0] in XY and c[1] == INSTR["AND"]:
        if c[0][1:] == "00":
            continue
        out = c[-1]
        for c_ in CONNS:
            # output from a x AND y gate should in turn be in an OR gate,
            # if not the case then add to swaps together with the output dest
            # of the x XOR y gate for the same x and y values (these two wires
            # require swapping).
            if out in [c_[0], c_[2]] and c_[1] != INSTR["OR"]:
                swaps.append(out)
                inps = [c[0], c[2]]
                other = next(
                    c__
                    for c__ in CONNS
                    if c__[0] in inps and c__[2] in inps and c__[1] == INSTR["XOR"]
                )
                swaps.append(other[-1])
                break

print(",".join(sorted(swaps)))
