"""Day 10: Factory

Part 2 drained most of what remained of my Christmas spirit after day 9.

part 1: 177mins
Wasn't going for speed. Spent time revising manipulation of bits.

part 2: Many many hours.
Ended up solving with simultaneous equations (took a while to write it and
then an age to get a couple of bugs out of it). Many of the machines have
more or the same number of buttons as counters - in which case there are
the same number or fewer unknowns than equations and these machines can
be solved simply (using sympy at least). Some machines have one more
button than counters, a fair few have two more and (in my data) four had
three more buttons than counters. In all these cases there are more
unknowns than there are equations and it's necessary to 'guess' the values
for 1, 2 or 3 of the unknowns (an unkonwn being how many times a button is
pressed). It's a matter of interating through all possible combinations of
values for the unknowns and singling out the solution that results in the
lowest number of overall presses. The number of iterations can be limted to
those values that are feasible in light of the maximum number of times a
button or combination of buttons could be pressed before one of the
counters goes over their target value.

NOTE: code assumes that all machines with one more button than counters
can be solved by assuming a value for just one variable. HOWEVER in my
data there was one such machine that requried the value of two unknowns to
be assumed (line 18) - this is why there's a hard-coded adjustment in
there. Anyone else using this code would need to first remove this
provision and then reinstate it according to what their own data throws up.

I think this is my longest aoc solution in terms of lines of code. In
theory it could be simplified with some refactoring, although eval and exec
don't play nicely when it comes to assigning variables in a function's
local scope.

It's also one of the longest for execution time too (80mins) - those 4
machines that require assuming values for 3 unknowns take an age.

(I initially appraoched this problem in a different way which worked off
part 1. I realised that the counters could be read as a single value, so
{3, 5, 4, 7} is 3547, and each button could be represented as a base 10
integer - for example if there are 8 counters and a button adds to counters
(0, 3, 4, 7) then the button can be expressed as 100110010, i.e. 306. If
this button were pressed 10 time's you'd reach 3060 and need 487 from the
other buttons to get to 3547. I used divmod to see how many times the
largest integer went into the value and then working with the next biggest
and from there iterating through possiblities until finding the target in
the minimum number of presses. Found it to be far more complicated than I'd
envisaged (worked for the example didn't scale) and ended up ditching the
approach in favour of simultaneous equations. If I'd have stuck my head up
earlier and taken an unprejudiced clean look at the problem I'd have
probably come round to simultaneous equations earlier.)

total: Many many hours.
18000
#linear-algebra
"""

import itertools

from collections import defaultdict, deque

from sympy import solve, Eq, symbols

from aocd import get_data as aocd_get_data


raw = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

# raw = aocd_get_data(day=10, year=2025)

lines_ = raw.splitlines()
lines_ = [line.split() for line in lines_]
lines = [[line[0]] + [line[1:-1]] + [line[-1]] for line in lines_]

# part 1
total = 0
for line in lines:
    # Works backwards from all lights being on to all lights being off.
    indicator_ = "".join("0" if c == "." else "1" for c in line[0][1:-1])
    indicator = int(indicator_, 2)
    buttons_ = [tuple(map(int, button[1:-1].split(","))) for button in line[1]]
    buttons_byte_strings = [
        "".join("1" if i in button else "0" for i in range(len(indicator_)))
        for button in buttons_
    ]
    buttons = [int(b, 2) for b in buttons_byte_strings]
    seen = set()
    queue = deque([(indicator, 0)])
    min_ = float("inf")
    while queue:
        lights, n = queue.popleft()
        if lights in seen or n >= min_:
            continue
        seen.add(lights)
        add = []
        break_ = False
        for b in buttons:
            nlights = lights ^ b
            if not nlights:
                min_ = min(min_, n + 1)
                break_ = True
                break
            add.append((nlights, n + 1))
        if not break_:
            queue.extend(add)

    total += min_

print(total)

# part 2

total = 0
for line_num, line in enumerate(lines):
    targets = tuple(map(int, line[-1][1:-1].split(",")))
    buttons = [
        (i, tuple(map(int, button[1:-1].split(","))))
        for i, button in enumerate(line[1])
    ]
    diff = len(buttons) - len(targets)
    print(f"\n{line_num=}, {targets=}, {buttons=}, {diff=}")

    # depending on how the variables relate to each other over the equestions, some
    # machines with the same number of buttons (or more) as counters still require
    # the value for one unknown to be assumed - it's easiest to just assume this is
    # the case for all of them.
    diff = max(diff, 1)
    if line_num in [18]:  # NOTE MANUAL INPUT
        # ...and in my input there was one line with only one fewer buttons than
        # counters which required values to be ascertained for two unknowns
        diff = 2

    # keys as counter indexes, values as list of buttons (as button indexes) that
    # augment the counter
    map_idx_to_buts = defaultdict(list)
    for i, b in buttons:
        for idx in b:
            map_idx_to_buts[idx].append(i)
    equations_base = []
    for idx, vals in map_idx_to_buts.items():
        # "xn" represents the number of times the button in index n needs to be pressed
        buts_for_idx = ["x" + str(v) for v in vals]
        equations_base.append((buts_for_idx, targets[idx]))

    it_limits = None
    it_limit_common = None
    
    if diff == 1:
        for i in range(len(buttons)):
            min_ = (float("inf"), {})
            vars = "x" + str(i)
            b = next(b for b in buttons if b[0] == i)
            it_limits = min(targets[idx] for idx in b[1])
            # it_limit = targets[0]  # A terrible bug in this original line meant I
            # wasn't always including values for the unknowns that should have been
            # included in the space of possibilities.

            # bring all symbols into scope except those in `vars`
            symbs = ["x" + str(i) for i in range(len(buttons)) if "x" + str(i) != vars]
            exec(f"{','.join(symbs)} = symbols('{' '.join(symbs)}')")

            break_ = False
            for a in range(it_limits + 1):
                exec(f"{vars} = a")
                equations = [
                    eval(f"Eq({'+'.join(unknowns)}, {t})") for unknowns, t in equations_base
                ]
                rtrn = solve(equations, eval(f"[{','.join(symbs)}]"))
                if not rtrn:
                    continue
                vals = rtrn.values()
                try:
                    if any(v < 0 or v != int(v) for v in rtrn.values()):
                        continue
                except Exception:
                    print(f"Breaking on error for vars: '{vars}'.")
                    break_ = True
                    break
                res = sum(vals) + a
                if min_[0] > res and int(res) == res:
                    button_presses = {int(str(k)[1:]): v for k, v in rtrn.items()}
                    button_presses[i] = a
                    min_ = (res, button_presses)
                    print(f"{line_num=}, {min_=}, {vars=}, {a=}")
            if not break_:  # have an answer
                break

    elif diff == 2:
        num_in_common = []
        for b, b2 in itertools.combinations(buttons, 2):
            n = len(set(b[1]) & set(b2[1]))
            num_in_common.append((n, b, b2))
        num_in_common.sort()

        while num_in_common:
            min_ = (float("inf"), {})
            _, *buts = num_in_common.pop()

            vars = ["x" + str(b[0]) for b in buts]
            it_limits = [min(targets[idx] for idx in but[1]) for but in buts]
            it_limit_common = min(
                targets[idx] for idx in set(buts[0][1]) & set(buts[1][1])
            )

            symbs = ["x" + str(i) for i in range(len(buttons)) if "x" + str(i) not in vars]
            exec(f"{','.join(symbs)} = symbols('{' '.join(symbs)}')")

            break_ = False
            for a in range(it_limits[0] + 1):
                for b in range(it_limits[1] + 1):
                    if it_limit_common is not None and a + b > it_limit_common:
                        continue
                    exec(f"{vars[0]} = a")
                    exec(f"{vars[1]} = b")
                    equations = [
                        eval(f"Eq({'+'.join(unknowns)}, {t})")
                        for unknowns, t in equations_base
                    ]

                    rtrn = solve(equations, eval(f"[{','.join(symbs)}]"))
                    if not rtrn:
                        continue
                    vals = rtrn.values()
                    try:
                        # One of the bugs I took an age to find was in here... I didn't
                        # realise that some of the returned values could include
                        # fractions, i.e. solutions that should have been rejected
                        # can't press a button 5 and a 1/3 times.
                        if any(v < 0 or v != int(v) for v in rtrn.values()):
                            continue
                    except Exception:
                        print(f"Breaking on error for vars: '{vars}'.")
                        break_ = True
                        break

                    res = sum(vals) + a + b
                    if res < min_[0] and int(res) == res:
                        button_presses = {int(str(k)[1:]): v for k, v in rtrn.items()}
                        button_presses[int(vars[0][1:])] = a
                        button_presses[int(vars[1][1:])] = b
                        min_ = (res, button_presses)
                        print(f"{line_num=}, {min_=}, {vars[0]=}, {a=}, {vars[1]=}, {b=}")
                if break_:
                    break
            if not break_:
                break

    elif diff == 3:

        num_in_common = []
        for b, b2, b3 in itertools.combinations(buttons, 3):
            n = len(set(b[1]) & set(b2[1]) & set(b3[1]))
            num_in_common.append((n, b, b2, b3))
        num_in_common.sort()

        while num_in_common:
            min_ = (float("inf"), {})
            _, *buts = num_in_common.pop()

            vars = ["x" + str(b[0]) for b in buts]
            it_limits = [min(targets[idx] for idx in but[1]) for but in buts]
            it_limit_common = min(
                targets[idx] for idx in set(buts[0][1]) & set(buts[1][1]) & set(buts[2][1])
            )

            symbs = ["x" + str(i) for i in range(len(buttons)) if "x" + str(i) not in vars]
            exec(f"{','.join(symbs)} = symbols('{' '.join(symbs)}')")

            break_ = False
            for a in range(it_limits[0] + 1):
                for b in range(it_limits[1] + 1):
                    for c in range(it_limits[2] + 1):
                        if it_limit_common is not None and a + b + c > it_limit_common:
                            continue
                        exec(f"{vars[0]} = a")
                        exec(f"{vars[1]} = b")
                        exec(f"{vars[2]} = c")
                        equations = [
                            eval(f"Eq({'+'.join(unknowns)}, {t})")
                            for unknowns, t in equations_base
                        ]

                        rtrn = solve(equations, eval(f"[{','.join(symbs)}]"))
                        if not rtrn:
                            continue
                        vals = rtrn.values()
                        try:
                            if any(v < 0 or v != int(v) for v in rtrn.values()):
                                continue
                        except Exception:
                            print(f"Breaking on error for vars: '{vars}'.")
                            break_ = True
                            break

                        res = sum(vals) + a + b + c
                        if res < min_[0] and int(res) == res:
                            button_presses = {int(str(k)[1:]): v for k, v in rtrn.items()}
                            button_presses[int(vars[0][1:])] = a
                            button_presses[int(vars[1][1:])] = b
                            button_presses[int(vars[2][1:])] = c
                            min_ = (res, button_presses)
                            print(
                                f"{line_num=}, {min_=}, {vars[0]=}, {a=},"
                                f" {vars[1]=}, {b=}, {vars[2]=}, {c=}"
                            )
                    if break_:
                        break
                if break_:
                    break
            if not break_:
                break

    ans, _button_presses = min_
    total += ans

print(f"{total=}")
