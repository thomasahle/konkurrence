import sys
from itertools import groupby
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

def sort(xs):
    if len(xs) <= 2:
        return xs
    a, b = xs[:2]
    xss = [[], [], []]
    for c in xs[2:]:
        i = median(a, c, b)
        xss[i].append(c)
    for sub in xss:
        sub[:] = sort(sub)
    # Flip first two lists by largest element
    for sub, up in zip(xss[:2], (a, b)):
        if len(sub) >= 2 and median(*sub[:2], up) == 0:
            sub[:] = sub[::-1]
    # Flip last list by smallest element
    sub = xss[2]
    if len(sub) >= 2 and median(b, *sub[:2]) == 2:
        sub[:] = sub[::-1]
    return xss[0] + [a] + xss[1] + [b] + xss[2]

def median(a, b, c):
    print(a, b, c, flush=True)
    med = int(sys.stdin.readline())
    #print(a, b, c, '-', med, file=sys.stderr, flush=True)
    return [a, b, c].index(med)

T, N, Q = read()
for case in range(T):
    res = sort(list(range(1,N+1)))
    print(' '.join(map(str, res)), flush=True)
    #print(' '.join(map(str, res)), file=sys.stderr)
    _ = read()
