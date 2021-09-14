# Lav om til linjestykker.
# To linjer (x,y0,y1) og (y,x0,x1) krydser når
# y0 <= y <= y1 og x0 <= x <= x1.
# Men selv da, hvordan ophæves dobeltkrydser?
# Hm, der er også det krav at det skal være et + og ikke bare at man rør.
# Så det kunne løses med
# y0 < y < y1 og x0 < x < x1.
# Men så virker det ikke når stregerne er opdelt...
# Set som en graf: Antal knuder med grad 4.

from typing import List
# Write any import statements here

def getPlusSignCount(N: int, L: List[int], D: str) -> int:
    hs, vs = [], []
    cur = (0, 0)
    for l, d in zip(L, D):
        if d == 'U': nxt = (cur[0], cur[1]-l)
        if d == 'D': nxt = (cur[0], cur[1]+l)
        if d == 'L': nxt = (cur[0]-l, cur[1])
        if d == 'R': nxt = (cur[0]+l, cur[1])
        if nxt[0] == cur[0]:
            # x, y0, y1
            vs.append((cur[0], min(cur[1], nxt[1]), max(cur[1], nxt[1])))
        if nxt[1] == cur[1]:
            # y, x0, x1
            hs.append((cur[1], min(cur[0], nxt[0]), max(cur[0], nxt[0])))
        cur = nxt

    # Compress coordinates to make the tree easier
    xs = {x for x,_,_ in vs} | {x0 for _,x0,_ in hs} | {x1 for _,_,x1 in hs}
    ys = {y for y,_,_ in hs} | {y0 for _,y0,_ in vs} | {y1 for _,_,y1 in vs}
    xmap = {x: i for i, x in enumerate(sorted(xs))}
    ymap = {y: i for i, y in enumerate(sorted(ys))}
    hs = [(ymap[y], xmap[x0], xmap[x1]) for y, x0, x1 in hs]
    vs = [(xmap[x], ymap[y0], ymap[y1]) for x, y0, y1 in vs]

    if not hs or not vs:
        return 0

    # Sort to group similar lines
    hs.sort()
    vs.sort()
    # Merge similar lines
    hs = merge(hs)
    vs = merge(vs)
    # Shrink by one to only count +'s
    hs = [(y, x0+1, x1-1) for y, x0, x1 in hs if x1-x0 >= 2]
    vs = [(x, y0+1, y1-1) for x, y0, y1 in vs if y1-y0 >= 2]

    # Create events for sweep line
    BEGIN, END, VERTICAL = 0, 2, 1
    events  = [(x0, BEGIN, y) for y, x0, x1 in hs]
    events += [(x1, END, y) for y, x0, x1 in hs]
    events += [(x, VERTICAL, y0, y1) for x, y0, y1 in vs]
    events.sort()

    # We need the size to be at least 3*MAX_N = 6,000,000
    fenwick = Fenwick(2**23)
    res = 0
    for ev in events:
        if ev[1] == END:
            fenwick.add(ev[2], -1)
        if ev[1] == VERTICAL:
            #res += fenwick.query(ev[2], ev[3])
            res += fenwick.prefix_sum(ev[3]+1) \
                   - fenwick.prefix_sum(ev[2])
        if ev[1] == BEGIN:
            fenwick.add(ev[2], 1)
    return res

def merge(segs):
    res = []
    cur = list(segs[0])
    for x, y0, y1 in segs[1:]:
        # Merge segments
        if x == cur[0] and y0 <= cur[2]:
            cur[2] = max(cur[2], y1)
        # New x
        else:
            res.append(cur)
            cur = [x, y0, y1]
    res.append(cur)
    return res

def brute(N, L, D):
    from collections import defaultdict
    edges = defaultdict(set)
    cur = (0, 0)
    for l, d in zip(L, D):
        if d in 'UD':
            dy = 1 if d == 'D' else -1
            for _ in range(l):
                nxt = (cur[0], cur[1]+dy)
                edges[cur].add(nxt)
                edges[nxt].add(cur)
                cur = nxt
        if d in 'LR':
            dx = 1 if d == 'R' else -1
            for _ in range(l):
                nxt = (cur[0]+dx, cur[1])
                edges[cur].add(nxt)
                edges[nxt].add(cur)
                cur = nxt
    return sum(bool(len(nbs)==4) for nbs in edges.values())


class Fenwick:
    def __init__(self, size):
        # Size should be a power of 2
        self.A = [0]*(size+1)
    def add(self, i, d):
        i += 1
        while i < len(self.A):
            self.A[i] += d
            i += i & (-i)
    def prefix_sum(self, i):
        # values [0, ... i-1]
        res = 0
        while i > 0:
            res += self.A[i]
            i -= i & (-i)
        return res

def test_fenwick():
    f = Fenwick(4)
    for i in range(4):
        f.add(i, i+1)
    for i in range(5):
        assert f.prefix_sum(i) == i*(i+1)//2

def test_cases():
    print(getPlusSignCount(9, [6, 3, 4, 5, 1, 6, 3, 3, 4], 'ULDRULURD'))
    print(getPlusSignCount(8, [1, 1, 1, 1, 1, 1, 1, 1], 'RDLUULDR'))
    print(getPlusSignCount(8, [1, 2, 2, 1, 1, 2, 2, 1], 'UDUDLRLR'))

def test_random():
    import random
    while True:
        N = random.randrange(2, 30)
        L = [random.randrange(10) for _ in range(N)]
        D = [random.choice('UDLR') for _ in range(N)]
        r1 = getPlusSignCount(N, L, D)
        r2 = brute(N, L, D)
        if r1 != r2:
            print(L, D)
            break

test_cases()
test_random()
