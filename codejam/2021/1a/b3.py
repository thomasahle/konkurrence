import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

from collections import Counter

def solve(pcnts):
    sum_ = sum(p*n for p, n in pcnts.items())
    for s in range(2, min(sum_, 5000)):
        s_copy = sum_ - s
        rs = 0
        for p, n in pcnts.items():
            i = 0
            while s_copy % p == 0:
                rs += p
                s_copy //= p
                i += 1
            if i > n:
                break
        else:
            if s_copy == 1 and rs == s:
                #print(s_copy, rs)
                # The first solution must be the best
                return sum_ - s
    return 0

T, = read()
for case in range(T):
    N, = read()
    cnt = Counter()
    for _ in range(N):
        p, n = read()
        cnt[p] += n
    res = solve(cnt)
    print(f'Case #{case+1}:', res)
