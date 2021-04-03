import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0
read_m1 = lambda: (int(x)-1 for x in sys.stdin.readline().split())
print_p1 = lambda xs: print(*(x+1 for x in xs))

from collections import defaultdict

N, T = read()

edges = defaultdict(list)
for _ in range(T):
    v1, v2 = read_m1()
    edges[v1].append(v2)
    edges[v2].append(v1)

stack = [0]
path = [0]
A = set(range(N)) - set([0])
B = set()
while len(A) != len(B):
    v = path[-1]
    i = stack[-1]
    #print('At', (v, i), edges[v])
    for j in range(i, len(edges[v])):
        v1 = edges[v][j]
        #print(v1, f'{v1 in A=}')
        if v1 in A:
            #print('Adding', v1, 'to path')
            path.append(v1)
            A.remove(v1)
            stack[-1] = j+1 # Save for next time
            stack.append(0)
            break
    # If we didn't find an A node, backtrack
    else:
        #print('Adding', v, 'to B')
        B.add(v)
        path.pop()
        stack.pop()

print(len(path), len(A))
print_p1(path)
print_p1(A)
print_p1(B)
