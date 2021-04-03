import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, = read()
xs = list(read())
xs.sort()
#print(xs[:N//2][::-1])
#print(xs[N//2:])
res = [x for pair in zip(xs[N//2:], xs[:N//2][::-1]) for x in pair]
if N % 2 != 0:
    res.append(xs[-1])
print(' '.join(map(str, res)))
