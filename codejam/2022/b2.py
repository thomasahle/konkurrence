import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

import random

def ab(xs):
    diag = sum(x**2 for x in xs)
    s = sum(x for x in xs)
    lower = (s**2 - diag) // 2
    return lower, s

def one_solve(xs):
    lower, s = ab(xs)
    if s == 0:
        if lower == 0:
            return 0
        return None
    if lower % s == 0:
        return -lower // s
    return None


def ksolve(a, b):
    return 1-b


def solve(xs, K):
    res = one_solve(xs)
    if res is not None:
        return [res]
    if K == 1:
        return None
    lower, s = ab(xs)
    x = ksolve(lower, s)
    if x is None:
        return None
    xs.append(x)
    res = one_solve(xs)
    return [x, res]

T, = read()
for case in range(T):
    N, K = read()
    xs = list(read())
    res = solve(xs, K)
    if res is None:
        res = 'IMPOSSIBLE'
    else: res = ' '.join(map(str, res))
    print(f'Case #{case+1}:', res)

