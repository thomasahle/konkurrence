import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

def solve(xs):
    res = 0
    for i in range(len(xs)-1):
        j = min(range(i,len(xs)), key=lambda j: xs[j])
        xs[i:j+1] = reversed(xs[i:j+1])
        res += j-i+1
    return res

T, = read()
for case in range(T):
    N, = read()
    xs = list(read())
    res = solve(xs)
    print(f'Case #{case+1}:', res)
