"""Day 10: Cathode-Ray Tube.

Part a 12 minutes, part b hours - CHECK ASSUMPTIONS ABOUT THE INPUT!!
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
outs, out = [], ""


def start_new_line():
    global out, outs, X
    outs.append(out)
    out = ""
    X += 40


def tick():
    global cyc, out
    out += "#" if X - 1 <= cyc <= X + 1 else "."
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

# make the output a bit prettier
outs_ = []
for out in outs:
    out_ = [out[i : i + 4] for i in range(0, len(out), 5)]
    out_ = "  ".join(out_)
    outs_.append(out_.replace(".", " "))
print("\n".join(outs_))
