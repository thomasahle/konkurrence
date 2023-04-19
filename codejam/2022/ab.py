import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

from collections import defaultdict, Counter

# AAAACCCC
# AAADDDD

import itertools
def chunk(w):
    it = itertools.groupby(w)
    for c, _ in it:
        yield c

def test(perm):
    seen = set()
    for c in chunk(''.join(perm)):
        if c in seen:
            return False
        seen.add(c)
    return True

def solve(ws):
    for perm in itertools.permutations(ws):
        if test(perm):
            return ''.join(perm)

T, = read()
for case in range(T):
    N, = read()
    xs = list(read(str))
    res = solve(xs)
    if res is None:
        res = 'IMPOSSIBLE'
    print(f'Case #{case+1}:', res)

