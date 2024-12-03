"""Day 3: Mull It Over

part a: 25mins
part b: 8mins

The best solution is to use a regex. I use them sufficiently little that I
thought it'd be quicker for me to just manipulate the string with standard
methods. (I've put up a `03_alt.py` version using a simple regex, so simple
in fact that I should have dared take this approach in the first place.)

total: 33mins, 9.8x bottom of the leaderboard.

#strings
"""

from aocd import get_data


raw = get_data(day=3, year=2024)

# raw = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""


def find_next_value(mem: str) -> tuple[int, str]:
    """Find value related to first "mul(" in `mem`.

    Returns
    -------
    value_mem: tuple[int, str]
        Two tuple where:
            [0] Value related to first "mul(" in `mem`
            [1] Remaining instruction in memory
    """
    idx_start = mem.find("mul(")
    mem = mem[idx_start + 4 :]
    idx_end = mem.find(")")
    if idx_end == -1:
        return 0, ""

    idx_nxt_start = mem.find("mul(")
    if idx_nxt_start != -1 and idx_nxt_start < idx_end:
        return 0, mem[idx_nxt_start:]

    op = mem[:idx_end]
    if "," not in op:
        return 0, mem[idx_end:]

    vals = op.split(",")
    if len(vals) != 2:
        return 0, mem[idx_end:]

    if not all(v.isdigit() for v in vals):
        return 0, mem[idx_end:]

    return int(vals[0]) * int(vals[1]), mem[idx_end:]


mem = raw
total = 0
while mem:
    v, mem = find_next_value(mem)
    total += v

print(total)

# raw = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

lines = [l.split("don't()")[0] for l in raw.split("do()")]
total = 0
for line in lines:
    mem = line
    while mem:
        v, mem = find_next_value(mem)
        total += v

print(total)
