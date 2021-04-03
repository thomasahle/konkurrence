import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0


N, M = read()
odds, evens = 0, 0
for _ in range(N):
    line = sys.stdin.readline()
    if line.count('1') % 2 == 0:
        evens += 1
    else: odds += 1

print(odds*evens)
