import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, = read()
A = read()
PRIME = 998244353

def dac(a, b):
    # Count the number of paths from the bottom of A[a] to the bottom of A[b]
    if a+2 == b:
        return 0
    if a+1 == b:
        return 0
    # Find the smallest in the interval
    p = min(range(a,b-1), key=lambda i: A[i])
    n1 = dac(a, b)
    n2 = dac(p, a)
    return n1 * n2 * A[p] % PRIME


