import sys
import random
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, = read()
ax, ay = read()
bx, by = read()
ax, ay, bx, by = ax-1, ay-1, bx-1, by-1
mvs = []
for _ in range(N):
    mvs.append(tuple(read()))

def is_reachable(x1,y1, x2,y2):
    reachable = set((x1+dx, y1+dy) for dx,dy in mvs
                    if 0 <= x1+dx < N and 0 <= y1+dy < N)
    if (x2,y2) in reachable:
        return True
    for dx,dy in mvs:
        if (x2-dx, y2-dy) in reachable:
            return True
    return False

if is_reachable(ax,ay, bx,by):
    print('Alice wins')
elif N <= 10:
    if all(is_reachable(bx,by, cx,cy) for cx in range(N) for cy in range(N)
            if (cx,cy) != (bx,by)):
        print('Bob wins')
    else:
        cx,cy = next((cx,cy) for cx in range(N) for cy in range(N)
                if (cx,cy) != (bx,by) and not is_reachable(bx,by,cx,cy))
        print('tie', cx+1, cy+1)
else:
    while True:
        cx, cy = random.randrange(N), random.randrange(N)
        if not is_reachable(bx,by, cx,cy):
            print('tie', cx+1, cy+1)
            break


