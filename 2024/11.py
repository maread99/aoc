"""Day 11: Plutonian Pebbles

part a: 18mins
Lost at least a few minutes trying to get out the example answer using
input for the first example rather than then later example that
corresponded with the example answer!

part b: 3 hours 32 minutes!
Oh my God. It really wasn't that complicated but it just did not come to
me. I first wondered if there was a pattern in the way the underlying data
grew. Then I spent an age struggling with trying to find some way to use
recurrsion with a cache, all based on the idea that most numbers come back
to themselves at some point and all big numbers end up breaking down into
smaller ones. But there were always 'new' large stone values that can crop
up (which is down that that crucial 'trailing zeros are ignored'). I
considered patterns for a bit, but that seemed to be just looking at the
same idea I had before from a different angle. I did step back a couple
of times to look at it a fresh, and doing so again brought about a rather
drawn out groan of realisation. Implementing the Counter solution took
less than ten minutes.

total: 3hours 50minutes! 33x bottom of the leaderboard. Horrendous.

#counter  #codify-rules
"""

from collections import Counter, defaultdict

from aocd import get_data

raw = get_data(day=11, year=2024)

# raw = "125 17"


def get_stones(v) -> list[int] | list[int, int]:
    s = str(v)
    if v == 0:
        return [1]
    elif len(s) % 2:
        return [v * 2024]
    else:
        stop = len(s) // 2
        return [int(s[:stop]), int(s[stop:])]


def count_stones(i: int):
    vals = [int(v) for v in raw.split()]
    cnt = Counter(vals)
    for _ in range(i):
        d = defaultdict(int)
        for k, v in cnt.items():
            nxt = get_stones(k)
            for n in nxt:
                d[n] += v
        cnt = Counter(d)
    return sum(cnt.values())


print(count_stones(25))
print(count_stones(75))
