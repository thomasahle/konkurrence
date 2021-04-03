import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, = read()
xvs = []
for _ in range(N):
    x, v = read()
    xvs.append((x, v))

crashes = []
for i, ((x1, v1), (x2, v2)) in enumerate(zip(xvs, xvs[1:])):
    if v1 <= v2:
        continue
    t = (x2 - x1) / (v1 - v2)
    crashes.append((t, i))

crashes.sort()
alive = set(range(N))
for _t, i in crashes:
    if i in alive and i+1 in alive:
        alive.remove(i)
        alive.remove(i+1)

print(len(alive))
print(' '.join(str(i+1) for i in sorted(alive)))
