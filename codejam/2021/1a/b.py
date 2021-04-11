import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

from itertools import chain, combinations
def subsets(iterable):
    xs = list(iterable)
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))


# Hvis jeg gerne vil højt op i prod er det bedre at tage nogle tal ca. i same størrelsesorden...

def solve(ps, ns):
    pns = [p for p, n in zip(ps, ns) for _ in range(n)]
    sum_ = sum(pns)
    best = 0
    for js in subsets(range(len(pns))):
        a, b = sum_, 1
        for j in js:
            a -= pns[j]
            b *= pns[j]
        if a == b:
            best = max(best, b)
    return best

T, = read()
for case in range(T):
    N, = read()
    ps, ns = [], []
    for _ in range(N):
        p, n = read()
        print(p, n)
        ps.append(p)
        ns.append(n)
    res = solve(ps, ns)
    print(f'Case #{case+1}:', res)
