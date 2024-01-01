"""Day 24: Never Tell Me The Odds

part a: 1hrs 50min
The noted careless bug probably cost me half hour

part b:
Bottom of the leaderboard took 1hr 2mins.

Dipped in and out of it as ideas occurred. Didn't get it out
without looking elsewhere.

Originally tried various ways of brute forcing the vector from possible
values. Evaluated the possible vectors as would be required to move from
one hailstone such that would hit another at a later nanosecond. Then
checked if the possible vectors intersected all other rays. Came out on the
example although too many possible combinations with the real data. Tried
all possible vectors between two random rays on the assumption that they
would both bit be hit within the first 10000ns. Got nothing.

Occurred that could just get the vector by considering parallel rays. The
plane between parallel rays represents all possible vectors. Get two
sets of parallel rays and where the planes intersect - that's your rock's
vector. Only issue, turns out that none of the rays in the real data are
parallel. Considered trying where only parallel in the x and y directions,
although doesn' come out, suspect because the resulting plane isn't a
plane at all but a twisted surface.

Looked for intersecting rays on the basis that, again, could then evaluate
a plane which would represent all possible vectors between those two rays.
Do the same for two sets of intersecting rays and then evaluate where those
planes intersect and that's the rock's vector. Alas, none of the rays
intersect.

Considered formulating an equation to describe a surface between lines
and seeing where other rays intersected it, although the world of
hyperbolas this seems to involve appears way beyond what aoc would ask for.

Wondered if it might be the eignvector but couldn't quite see how.

Chucked the example into Blender with Sverchok to be able to visualise what
was going on. Didn't help.

Turns out most people see to have solved by solving simulataneous
equations. I had considered this from the off although was unable to get
equations into a form that could be solved with np.linalg. If I'd have been
familiar with sympy I might have got this one out. I was on the right
tracks with assuming would require three lines to solve. Can either solve
9 equations for the six required unknowns plus three variables representing
the time until collision (one for each of the three lines) or can eliminate
time from the equations and solve six equations directly for the six
unknowns (i.e. each of the three components of the position and each of the
vector).

Served to discover / learn a bit of sympy!

#vectors #systems #linear-algebra

-- Alternative Approach --
I did come accross a solution or two that solved within the confines of
the standard library, of note:
    https://github.com/mebeim/aoc/blob/master/2023/solutions/day24.py
@mebeim solved on the following basis (I'm not clear on what's going on
here):
    (p - a) X (v - va) == (p - b) X (v - vb)
Is it defining two lines as (r - p) X d = 0 and setting them against each
other? From there resolves with matrix operations.
Suspect that the following solution works along similar lines...
    https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kersplf/
"""

import itertools

import numpy as np
import sympy
from aocd import get_data

raw = get_data(day=24, year=2023)

BOUND_LOW = 200000000000000
BOUND_HIGH = 400000000000000


# raw = """19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3
# """

# BOUND_LOW = 7
# BOUND_HIGH = 20


lines = raw.splitlines()

# tuple of px, py, pz, vx, vy, vz
Point = tuple[int, int, int]
Vector = tuple[int, int, int]
Ray = tuple[Point, Vector]

rays: list[Ray] = []
for line in lines:
    ps, vs = line.split(" @ ")
    rays.append((tuple(map(int, ps.split(","))), tuple(map(int, vs.split(",")))))


def intersect(a: Ray, b: Ray) -> bool:
    (apx, apy, _), (avx, avy, _) = a
    (bpx, bpy, _), (bvx, bvy, _) = b

    px = apx - bpx
    py = apy - bpy

    # Solve system of equations
    a_ = np.array([[-avx, bvx], [-avy, bvy]])
    b_ = np.array([px, py])
    try:
        landa_a, landa_b = np.linalg.solve(a_, b_)
    except np.linalg.LinAlgError:
        return False

    if (landa_a < 0) or (landa_b < 0):
        return False

    x = (landa_a * avx) + apx
    # y = (landa_b * bvx) + bpx   # NB careless initial bug
    y = (landa_b * bvy) + bpy  # Corrected

    return (BOUND_LOW <= x <= BOUND_HIGH) and (BOUND_LOW <= y <= BOUND_HIGH)


ans = sum(intersect(a, b) for a, b in itertools.combinations(rays, 2))
print(ans)

# part b

a, b, c = rays[:3]
(apx, apy, apz), (avx, avy, avz) = a
(bpx, bpy, bpz), (bvx, bvy, bvz) = b
(cpx, cpy, cpz), (cvx, cvy, cvz) = c

px, py, pz, vx, vy, vz, ta, tb, tc = sympy.symbols("px, py, pz, vx, vy, vz, ta, tb, tc")

equations = [
    sympy.Eq(apx + ta * avx, px + ta * vx),
    sympy.Eq(apy + ta * avy, py + ta * vy),
    sympy.Eq(apz + ta * avz, pz + ta * vz),

    sympy.Eq(bpx + tb * bvx, px + tb * vx),
    sympy.Eq(bpy + tb * bvy, py + tb * vy),
    sympy.Eq(bpz + tb * bvz, pz + tb * vz),

    sympy.Eq(cpx + tc * cvx, px + tc * vx),
    sympy.Eq(cpy + tc * cvy, py + tc * vy),
    sympy.Eq(cpz + tc * cvz, pz + tc * vz),
]

# alternative six equation solution which sets equations to time and then
# against each other.
# equations = [
#     sympy.Eq((apx - px) * (vy - avy), (apy - py) * (vx - avx)),
#     sympy.Eq((apx - px) * (vz - avz), (apz - pz) * (vx - avx)),
# 
#     sympy.Eq((bpx - px) * (vy - bvy), (bpy - py) * (vx - bvx)),
#     sympy.Eq((bpx - px) * (vz - bvz), (bpz - pz) * (vx - bvx)),
# 
#     sympy.Eq((cpx - px) * (vy - cvy), (cpy - py) * (vx - cvx)),
#     sympy.Eq((cpx - px) * (vz - cvz), (cpz - pz) * (vx - cvx)),
# ]

print(sum(sympy.solve(equations, [px, py, pz, vx, vy, vz, ta, tb, tc])[0][:3]))
