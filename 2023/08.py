"""Day 8: Haunted Wasteland

part a: 13mins

part b: 71mins
Interrogation of the paths unearthed that the path from each start node
would only ever pass through ONE of the end nodes, and that it would do
so periodically. Accordingly the solution is the step when the patterns
coincide for all start nodes, i.e. the lowest common multiple of the counts
for each.

Took longer than I needed to have on part b due to abandoning an earlier
more general implementation which assumed that a path's loop could pass
through any number of end nodes before repeating. It identifed the pattern
by looking for the first occassion that were back at a previously seen node
with the same prior 277 moves (the number of moves in the unique cycle).
It should have come out although had a careless bug that was resulting in a
MemoryError. POOR DEBUGGING - should have spotted it at the time..
    seen.add(nnode, moves_to_date[:-NUM_MOVES]) # bug, taking all but the last 277 chars
    seen.add(nnode, moves_to_date[-NUM_MOVES:]) # correct, taking the last 277 chars
NB: If it were the case that a path could go through various end nodes then
believe that, after identifying the pattern, it would be necessary to
evaluate the steps on which each end node on the path was being hit (for
each start node) and the solution would then be the minimum LCM of all the
possible combinations of when the end nodes synchronised.
    
total: 84mins, 8.5x bottom of the leaderboard.

#lcm
"""

import itertools
import math

from aocd import get_data

raw = get_data(day=8, year=2023)

lines = raw.splitlines()

moves = itertools.cycle(lines[0])
nodes = [node.split() for node in lines[2:]]

# node: (next_node_left, next_node_right)
NODES = {node[0]: (node[2][1:-1], node[3][:-1]) for node in nodes}

# part a

count = 0
nnode = "AAA"
for move in moves:
    node = NODES[nnode]
    nnode = node[0] if move == "L" else node[1]
    count += 1
    if nnode == "ZZZ":
        break

print(count)

# part b

moves = itertools.cycle(lines[0])

STARTS = [node for node in NODES if node.endswith("A")]
ENDS = [node for node in NODES if node.endswith("Z")]

end_counts = []
for start in STARTS:
    nnode = start
    count = 0
    for move in moves:
        node = NODES[nnode]
        nnode = node[0] if move == "L" else node[1]
        count += 1
        if nnode in ENDS:
            end_counts.append(count)
            break

print(math.lcm(*end_counts))
