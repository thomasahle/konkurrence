import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, K, = read()
x, y = read()

# 0 < k < n
res = (N*x - K*y)/(N-K)
if res < 0 or res > 100:
    print('impossible')
else:
    print(res)
