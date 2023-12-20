"""Day 20: Pulse Propagation

part a: 3hrs 20
Took a while to get my head around what was actually going on. Then
had a couple of initial bugs (as noted in the comments).

part b: 2hrs
Spent time checking that it wasn't a simple solve and just not coming out
as a result of a hidden bug in part a. No such luck. It wouldn't have come
out for over 200 trillion cycles!

Grateful at least that the patterns for the feeder modules all coincided
from the first cycle!

total: 5hrs 20mins, 6.5x bottom of the leaderboard.

#classes  #queue
"""

from __future__ import annotations

import math
from collections import defaultdict, deque

from aocd import get_data

raw = get_data(day=20, year=2023)

# raw = r"""broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a
# """

# raw = r"""broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output
# """

lines = raw.splitlines()

HIGH, LOW = True, False


class Mod:
    def __init__(self, name: str):
        self.name = name
        self.ds: list[Mod] = []

    def set_destinations(self, ds: list[Mod]):
        self.ds = ds

    def receive(self, pulse: bool, frm: Mod):
        """Operate on receiving a pulse."""
        self.emit(pulse)

    def emit(self, pulse: bool):
        for d in self.ds:
            QUEUE.append((d, pulse, self))

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__},"
            f" {self.name.upper()},"
            f" ds: {[d.name for d in self.ds]}>"
        )


class FlipFlop(Mod):
    def __init__(self, name):
        super().__init__(name)
        self.is_on = False

    def receive(self, pulse: bool, frm: Mod):
        # NOTE initial bug didn't account for doing nothing if pulse was high
        if pulse is HIGH:
            return
        self.is_on = not self.is_on
        pulse = HIGH if self.is_on else LOW
        self.emit(pulse)


class Conjunction(Mod):
    def __init__(self, name):
        super().__init__(name)
        self.memory = {}

    def add_input(self, inp: Mod):
        self.memory[inp] = LOW

    def receive(self, pulse: bool, frm: Mod):
        self.memory[frm] = pulse
        pulse = LOW if all(self.memory.values()) else HIGH
        self.emit(pulse)

    def __repr__(self) -> str:
        return super().__repr__() + f", inputs: {[inp.name for inp in self.memory]}"


def create_mods() -> dict[str, Mod]:
    mods: dict[str, Mod] = {}

    # initial sweep to create all modules
    for line in lines:
        typ_name, _ = line.split(" -> ")
        typ, name = typ_name[0], typ_name[1:]
        if typ_name == "broadcaster":
            mods[typ_name] = Mod("broadcaster")
        elif typ == "&":
            mods[name] = Conjunction(name)
        else:
            assert typ == "%"
            mods[name] = FlipFlop(name)

    # second sweep to set destination modules and, for Conjuction mods, inputs.
    for line in lines:
        typ_name, ds_ = line.split(" -> ")
        name = typ_name if typ_name == "broadcaster" else typ_name[1:]
        ds = []
        for d in ds_.split(", "):
            if d not in mods:
                mods[d] = Mod(d)  # modules that don't emit, only receive ("rx")
            mod = mods[d]
            ds.append(mods[d])
            # NOTE initial bug...
            # if isinstance(d, Conjunction): # careless
            if isinstance(mod, Conjunction):  # corrected
                mod.add_input(mods[name])
        mods[name].set_destinations(ds)

    return mods


# part a

MODS = create_mods()
# tuples of (receiving mod_, pulse_is_high, emitting mod)
QUEUE: deque[tuple[Mod, bool, Mod]] = deque()

count_high = 0
count_low = 0
CYCLES = 1000
for _ in range(CYCLES):
    MODS["broadcaster"].receive(LOW, "button")
    count_low += 1
    while QUEUE:
        to_mod, pulse_is_high, frm_mod = QUEUE.popleft()
        # high_low = "HIGH" if pulse_is_high else "LOW"  # DEBUG LINES
        # print(f"from {frm_mod.name.upper()} {high_low} to {to_mod.name.upper()}")
        to_mod.receive(pulse_is_high, frm_mod)
        if pulse_is_high:
            count_high += 1
        else:
            count_low += 1

print((count_low) * (count_high))

# part b

MODS = create_mods()
QUEUE = deque()  # tuples of (receiving mod_, pulse_is_high, emitting mod)

# Assert that only one module emits to 'rx'.
feeder_mods = [mod for mod in MODS.values() if MODS["rx"] in mod.ds]
assert len(feeder_mods) == 1
feeder_mod = feeder_mods[0]

cycs: dict[str, list] = defaultdict(list)
cyc = 0
while True:
    cyc += 1
    MODS["broadcaster"].receive(LOW, "button")
    broke = False
    while QUEUE:
        to_mod, pulse_is_high, frm_mod = QUEUE.popleft()
        if to_mod is feeder_mod and pulse_is_high:
            cycs[frm_mod.name].append(cyc)
            if all(len(vals) == 2 for vals in cycs.values()):
                broke = True
                break
        to_mod.receive(pulse_is_high, frm_mod)
    if broke:
        break

# assert pattern repeats from first cycle for all modules that emit to feeder
# NOTE: this should be common to all input data
assert all(vals[0] == (vals[1] - vals[0]) for vals in cycs.values())

pat_lens = [cycs[mod][0] for mod in cycs]
print(math.lcm(*pat_lens))
