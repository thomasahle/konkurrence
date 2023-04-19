import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0


def solve(xs):
    diag = sum(x**2 for x in xs)
    s = sum(x for x in xs)
    lower = (s**2 - diag) // 2
    if s == 0:
        if lower == 0:
            return 0
        return None
    if lower % s == 0:
        return -lower // s


T, = read()
for case in range(T):
    N, K = read()
    xs = list(read())
    res = solve(xs)
    if res is None:
        res = 'IMPOSSIBLE'
    print(f'Case #{case+1}:', res)

