"""Day 10: Cathode-Ray Tube.

Print-as-you-go.
"""

from aocd import get_data

raw = get_data(day=10, year=2022)

data = raw.splitlines()

X = 1
cyc = 0
r = [20, 60, 100, 140, 180, 220]
s = []


def tick():
    global cyc, s
    cyc += 1
    if cyc in r:
        s.append(cyc * X)


for line in data:
    if " " not in line:
        tick()
    else:
        v = int(line.split()[1])
        tick()
        tick()
        X += v
print(sum(s), "\n")


# part b

X = 1
cyc = 0
LINE_ENDS = list(range(40, 241, 40))


def start_new_line():
    global X
    print("")
    X += 40


def tick():
    global cyc
    print("#" if X - 1 <= cyc <= X + 1 else ".", end="")
    cyc += 1
    if cyc in LINE_ENDS:
        start_new_line()

for line in data:
    if " " not in line:
        tick()
    else:
        v = int(line.split()[1])
        tick()
        tick()
        X += v
