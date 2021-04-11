import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

def solve(ps, ns):
    pns = [p for p, n in zip(ps, ns) for _ in range(n)]
    sum_ = sum(pns)
    best = 0
    for rhsize in range(len(pns)+1):
        for sub_ps in combinations(pns, rhsize):
            a, b = sum_, 1
            for p in sub_ps:
                a -= p
                b *= p
            if a == b:
                best = max(best, b)
            if b > 500*a:
                #print(b, a)
                return best
    return 0

T, = read()
for case in range(T):
    N, = read()
    ps, ns = [], []
    for _ in range(N):
        p, n = read()
        #print(p, n)
        ps.append(p)
        ns.append(n)
    res = solve(ps, ns)
    print(f'Case #{case+1}:', res)
