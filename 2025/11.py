"""Day 11: Reactor

part 1: 20mins

part 2: 3hr 30mins
Tried various DFS approaches before hitting on first working backwards to
identify the whole graph structure in terms of the nodes that fall 'after'
each node. From here was able break the task down into three legs:
    from svr to fft
    from fft to dac
    from dac to out
...and optimise the evalution of the number of paths for each leg by only
considering those paths that stuck within the known space. Comes out in
<10s (on my machine).

NOTE: Solution assumes paths see "fft" before "dac", i.e. as in the
example (and as for my input).

EDIT: My word, not sure why I ended up complicating this so much. It can be
solved with a simple cached DFS - see 11_rev.py.

total: 3h 50mins
9787
#DFS  #sets
"""

from aocd import get_data

raw = get_data(day=11, year=2025)

# raw = """aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out
# """

# raw = """svr: aaa bbb
# aaa: fft
# fft: ccc
# bbb: tty
# tty: ccc
# ccc: ddd eee
# ddd: hub
# hub: fff
# eee: dac
# dac: fff
# fff: ggg hhh
# ggg: out
# hhh: out
# """

lines = raw.splitlines()

NETWORK = {}
for line in lines:
    k, v = line.split(": ")
    NETWORK[k] = v.split()

# part 1

PATHS: list[list] = [["you"]]

total1 = 0
while PATHS:
    path = PATHS.pop()
    for n in NETWORK[path[-1]]:
        if n == "out":
            total1 += 1
            continue
        PATHS.append(path + [n])

print(total1)

# part 2

# dict with keys as nodes and values as all nodes that fall after the key
# on the path from 'key' to 'out'
nodes_under = {k: {"out"} for k, v in NETWORK.items() if "out" in v}
while len(nodes_under) < len(NETWORK):
    for k, v in NETWORK.items():
        if all(n in nodes_under for n in v):
            under = set(v)
            for n in v:
                under |= nodes_under[n]
            nodes_under[k] = under

assert len(nodes_under["svr"]) == len(lines)


def num_paths(frm: str, to: str, subset: set[str] | None = None) -> int:
    """Return number of paths from `frm` to `to`.

    If `subset` passed then will not follow any paths that deviate from
    the space described by `subset`.
    """
    paths: list[list] = [[frm]]
    total = 0
    while paths:
        path = paths.pop()
        for n in NETWORK[path[-1]]:
            if n == to:
                total += 1
                continue
            if subset is not None and n not in subset:
                continue
            paths.append(path + [n])
    return total

# nodes from which path has to pass through 'fft' to reach 'out'
fft_under = {k for k, v in nodes_under.items() if "fft" in v}
num = num_paths("svr", "fft", subset=fft_under)
# nodes from which path has to pass through 'dac' to reach 'out'
dac_under = {k for k, v in nodes_under.items() if "dac" in v}
num *= num_paths("fft", "dac", subset=dac_under)
num *= num_paths("dac", "out")
print(num)
