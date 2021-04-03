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
    #print('adding', t, i, j)
    heappush(crashes, (t, i, j))

for i in range(N):
    add(i, i+1)

nxt = {i:i+1 for i in range(N)}
prv = {i:i-1 for i in range(N)}
alive = set(range(N))
while crashes:
    _t, i, j = heappop(crashes)
    if i in alive and j in alive:
        alive.remove(i)
        alive.remove(j)
        #print('kill', i, j, 'at', _t)
        # No, we need to add the actual first alive to the left and right.
        #i1 = i-1
        #while i1 != -1 and i1 not in alive:
            #i1 -= 1
        #j1 = j+1
        #while j1 != N and j1 not in alive:
            #j1 += 1
        i1 = prv[i]
        j1 = nxt[j]
        #print('add', i1, j1)
        add(i1, j1)
        nxt[i1] = j1
        prv[j1] = i1

print(len(alive))
print(' '.join(str(i+1) for i in sorted(alive)))
