import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, = read()
C = []
for _ in range(N):
    C.append(list(read()))

As = [0]
for i in range(1, N):
    row = [C[i][j]-C[0][j] for j in range(N)]
    if len(set(row)) != 1:
        print('No')
        sys.exit()
    As.append(row[0])

shift = min(As)
for i in range(N):
    As[i] -= shift

Bs = [C[0][j] - As[0] for j in range(N)]

print('Yes')
print(' '.join(map(str, As)))
print(' '.join(map(str, Bs)))
