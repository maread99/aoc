"""Day 16: Proboscidea Volcanium

Didn't get part a of this one out. Mistakenly gave up on a brute force
solution on seeing the number of combinations involved. Although I was
aware of the need to focus on only the open valves, for some reason failed
to simplify the question to distances between them. This implementation is
heavily inspired by hyper-nutrino's solution:
    https://github.com/hyper-neutrino/advent-of-code/blob/main/2022/day16p1.py
...which in turn was inspired by betaveros's solution:
    https://github.com/betaveros/advent-of-code-2022/blob/main/p16.noul

Did get part b out by building on part a, albeit with a solution that took
60s even with the cache.
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


def dfs_a(v, tm, states):
    max_ = 0

    for nv, d in dists[v].items():
        mask = 1 << indices[nv]
        if states & mask:
            continue  # nv is already open
        ntm = tm - d - 1
        if ntm < 1:
            continue
        max_ = max(max_, dfs_a(nv, ntm, states | mask) + ntm * FLOWS[nv])

    return max_


print(dfs_a("AA", 30, 0))


# part b, 60s with cache, 130s without
cache = {}


def dfs_b(v, vE, tm, tmE, states):
    max_ = 0

    if (tup := (v, vE, tm, tmE, states)) in cache:
        return cache[tup]

    for nv, d in dists[v].items():
        mask = 1 << indices[nv]
        if states & mask:
            continue  # nv is already open
        ntm = tm - d - 1
        if ntm < 1:
            continue
        nstates = states | mask

        for nvE, d in dists[vE].items():
            mask = 1 << indices[nvE]
            if nstates & mask:
                continue  # nv is already open
            ntmE = tmE - d - 1
            if ntmE < 1:
                continue
            flows = (ntm * FLOWS[nv]) + (ntmE * FLOWS[nvE])
            max_ = max(max_, dfs_b(nv, nvE, ntm, ntmE, nstates | mask) + flows)

    cache[(v, vE, tm, tmE, states)] = max_

    return max_


print(dfs_b("AA", "AA", 26, 26, 0))
