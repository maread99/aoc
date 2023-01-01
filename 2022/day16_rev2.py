"""Day 16: Proboscidea Volcanium

Improved part b, as hyper-nutrino's solution:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day16p2.py
Simply takes the maximum result of all possible distributions of valves
between the two parties.
"""

from collections import defaultdict, deque
import itertools
import re

from aocd import get_data


raw = get_data(day=16, year=2022)


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"(?:(?<!\d)-)?\d+", s)))


GRAPH: dict[str, list[str]] = {}
FLOWS: dict[str, int] = {}
for line in raw.splitlines():  # example_lines:  # raw.splitlines()
    parts = line.split()
    v = parts[1]
    adj = [p.strip(",") for p in parts[2:] if p.isupper()]
    GRAPH[v] = adj
    FLOWS[v] = ints(line)[0]


def shortest_path(a, b) -> list[str]:
    """Shortest path between two nodes"""
    q = deque([[a]])
    seen = set()
    while q:
        path = q.popleft()
        for nv in GRAPH[path[-1]]:
            if nv in seen:
                continue
            np = path + [nv]
            if nv == b:
                return np
            seen.add(nv)
            q.append(np)
    raise Exception()


non_zero_valves = {k for k, v in FLOWS.items() if v}


# shortest_paths_between non_zero valves
dists = defaultdict(dict)
for a, b in list(itertools.product(non_zero_valves | {"AA"}, non_zero_valves)):
    if a == b:
        continue
    path = shortest_path(a, b)
    dists[a][b] = len(path) - 1


indices = {k: i for i, k in enumerate(non_zero_valves)}


cache ={}

def dfs(v, tm, states):
    max_ = 0
    
    if (key := (v, tm, states)) in cache:
        return cache[key]

    for nv, d in dists[v].items():
        mask = 1 << indices[nv]
        if states & mask:
            continue  # nv is already open
        ntm = tm - d - 1
        if ntm < 1:
            continue
        max_ = max(max_, dfs(nv, ntm, states | mask) + ntm * FLOWS[nv])

    cache[key] = max_

    return max_


print(dfs("AA", 30, 0))

bm_all_closed = (1 << len(non_zero_valves)) - 1

max_ = 0
for i in range((bm_all_closed // 2) + 1):
    max_ = max(max_, dfs("AA", 26, i) + dfs("AA", 26, bm_all_closed ^ i))

print(max_)
