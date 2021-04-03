import sys
from itertools import groupby
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

def solve(X, Y, cjs):
    rle = [c for c,run in groupby(cjs) if c != '?']
    res = 0
    for c0, c1, in zip(rle, rle[1:]):
        if c0+c1 == 'CJ':
            res += X
        if c0+c1 == 'JC':
            res += Y
    return res

T, = read()
for case in range(T):
    X, Y, cjs, = read(str)
    X, Y = int(X), int(Y)
    res = solve(X, Y, cjs)
    print(f'Case #{case+1}:', res)
