
from typing import List
import bisect

# fn(u) = min_{x in [1,u]}  f_{n-1}(x-1)
#                         + A [x < ai] (ai - x)
#                         + B [x > ai] (x - ai)

def getMinimumSecondsRequired(N: int, R: List[int], A: int, B: int) -> int:
    inf = 10**15
    def f(l, u):
        xs = [x for x,_ in l]
        vs = [v for _,v in l]
        i = bisect.bisect(xs, u)
        if i == 0: return inf
        if i == len(xs): return vs[-1]
        x0, a = l[i-1]
        x1, b = l[i]
        return a + (b-a)*(u-x0)//(x1-x0)

    l = [(0, 0)]
    for r in R:
        # Shift f by 1
        l = [(x+1, v) for x, v in l]

        # If x <= r, set R=r
        l0 = [(x, v + (r-x)*B) for x,v in l if x <= r]
        l0.append((r, f(l,r)))

        # Lidt extra område hvor vi også skubber r op
        vm, xm = min((v+(x-r)*A, x) for x, v in [(r, f(l,r))] + l if x >= r)
        #vm, xm = min((f(l,x)+(x-r)*A, x) for x in [r]+[x for x,v in l if x > r])
        l0 += [(x, v + (x-r)*A) for x,v in l if r < x <= xm]

        l = l0

    return l[-1][1]

def bf(N: int, R: List[int], A: int, B: int) -> int:
    def f(i, u):
        if i < 0: return 0
        return min((f(i-1, x-1)
                   + bool(x < R[i])*(R[i] - x) * B
                   + bool(x > R[i])*(x - R[i]) * A
                for x in range(1, u+1)),
                default=30)
    return f(N-1, 30)

def bf2(N: int, R: List[int], A: int, B: int) -> int:
    import itertools
    best = 10**12
    for perm in itertools.combinations(range(1, max(R)+N), N):
        price = sum(
                   bool(p < r)*(r - p) * B + # Deflate down to p
                   bool(p > r)*(p - r) * A   # Inflate up to p
                   for r, p in zip(R, perm))
        best = min(best, price)
    return best

import random
N = 5
A, B = 2, 1
while True:
    R = [random.randrange(1,7) for _ in range(N)]
    print(R)
    r1 = getMinimumSecondsRequired(N, R, A, B)
    r2 = bf(N, R, A, B)
    r3 = bf2(N, R, A, B)
    if r1 != r2 or r1 != r3:
        print(R)
        print(r1, r2, r3)
        break

#print(getMinimumSecondsRequired(0, [6, 5, 4, 3], 1, 1))
#print(getMinimumSecondsRequired(0, [2, 5, 3, 6, 5], 1, 1))
#print(getMinimumSecondsRequired(0, [100, 100, 100], 2, 3))
#print(getMinimumSecondsRequired(0, [100, 100, 100], 7, 3))
#print(getMinimumSecondsRequired(0, [6, 5, 4, 3], 10, 1))
#print(getMinimumSecondsRequired(0, [100, 100, 1, 1], 2, 1))
#print(getMinimumSecondsRequired(0, [6,5,2,4,4,7], 1, 1))
