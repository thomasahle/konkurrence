import sys
from itertools import groupby
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

def inner(N, C):
    assert N-1 <= C <= (N+1)*N//2-1
    if N == 1:
        return [0]
    # Pick k in [1,N] such that
    # N-2 <= C-k <= N*(N-1)//2-1
    # kmax = min(C-N+2, N)
    # kmin = max(C-N*(N-1)//2+1, 1)
    k = min(C-N+2, N)
    seq = [i+1 for i in inner(N-1, C-k)]
    seq = seq[:k-1][::-1] + [0] + seq[k-1:]
    return seq

def solve(N, C):
    if not N-1 <= C < (N+1)*N//2:
        return 'IMPOSSIBLE'
    res = inner(N, C)
    return ' '.join(str(i+1) for i in res)

T, = read()
for case in range(T):
    N, C = read()
    res = solve(N, C)
    print(f'Case #{case+1}:', res)
