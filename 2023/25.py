"""Day 25: Snowverload

part a: few hours probably.
Started with a brute force approach. Ditched it before even trying to
optimize. Sketched out the example graph. From that tried to work out ways
to approach it. Came up with nothing that I wasn't able to discard within
about thirty seconds. Wondered if it could be visualised in bqplot. It
could! See `25.ipynb`. Got the wires to cut from inspection of this
visualization.

#graph
"""

from collections import defaultdict

from aocd import get_data

raw = get_data(day=25, year=2023)

raw = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

lines = raw.splitlines()

MAP: dict[str, set[str]] = defaultdict(set)
for line in lines:
    lhs, rhs_ = line.split(":")
    rhs = set(rhs_.split())
    MAP[lhs] |= rhs
    for k in rhs:
        MAP[k].add(lhs)


# wires to disconnect by inspection of graph created in `25.ipynb`
wires = ("hfx", "pzl"), ("bvb", "cmg"), ("nvd", "jqt")  # for example
# wires = ("qnv", "mnh"), ("ljh", "tbg"), ("ffv", "mfs")  # for my input

# disconnect wires
MAP[wires[0][0]].remove(wires[0][1])
MAP[wires[1][0]].remove(wires[1][1])
MAP[wires[2][0]].remove(wires[2][1])
MAP[wires[0][1]].remove(wires[0][0])
MAP[wires[1][1]].remove(wires[1][0])
MAP[wires[2][1]].remove(wires[2][0])

# collect nodes in one part of the cut graph
seen = set()
nodes = MAP[wires[0][0]].copy()
while nodes:
    n = nodes.pop()
    nnodes = MAP[n]
    for nnode in nnodes:
        if nnode in seen:
            continue
        nodes.add(nnode)
    seen.add(n)

print(len(seen) * (len(MAP) - len(seen)))
