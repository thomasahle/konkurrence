import sys
from heapq import heappush, heappop
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, = read()
xvs = []
for _ in range(N):
    x, v = read()
    xvs.append((x, v))

crashes = []
def add(i, j):
    if i < 0 or j >= N:
        return
    x1, v1 = xvs[i]
    x2, v2 = xvs[j]
    if v1 == v2:
        return
    t = (x2 - x1) / (v1 - v2)
    if t <= 0:
        return
    heappush(crashes, (t, i, j))

for i in range(N):
    for j in range(i+1, N):
        add(i, j)

alive = set(range(N))
while crashes:
    _t, i, j = heappop(crashes)
    if i in alive and j in alive:
        alive.remove(i)
        alive.remove(j)
        print('kill', i, j, 'at', _t)

print(len(alive))
print(' '.join(str(i+1) for i in sorted(alive)))
