from typing import List
from collections import defaultdict, deque

def getSecondsRequired(R: int, C: int, G: List[List[str]]) -> int:
    portals = defaultdict(list)
    start = None
    for y, row in enumerate(G):
        for x, c in enumerate(row):
            if ord('a') <= ord(c) <= ord('z'):
                portals[c].append((y,x))
            if c == 'S':
                start = (y,x)

    q = deque([(start,0)])
    visited = set([start])
    res = -1
    while q:
        (py, px), d = q.popleft()
        if G[py][px] == 'E':
            res = d
            break
        candidates = []
        for dy, dx in [(-1,0), (0,1), (1,0), (0,-1)]:
            p1 = (p1y, p1x) = (py+dy, px+dx)
            if 0 <= p1y < R and 0 <= p1x < C \
                    and G[p1y][p1x] != '#' and p1 not in visited:
                visited.add(p1)
                q.append((p1, d+1))
        if G[py][px] in portals:
            for p1 in portals[G[py][px]]:
                if p1 not in visited:
                    visited.add(p1)
                    q.append((p1, d+1))
    return res

from typing import List
from collections import defaultdict, deque

def getSecondsRequired(R: int, C: int, G: List[List[str]]) -> int:
    portals = defaultdict(list)
    start = None
    for y, row in enumerate(G):
        for x, c in enumerate(row):
            if ord('a') <= ord(c) <= ord('z'):
                portals[c].append((y,x))
            if c == 'S':
                start = (y,x)

    q = deque([(start,0)])
    visited = set([start])
    res = -1
    while q:
        (py, px), d = q.popleft()
        if G[py][px] == 'E':
            res = d
            break
        candidates = []
        for dy, dx in [(-1,0), (0,1), (1,0), (0,-1)]:
            p1 = (p1y, p1x) = (py+dy, px+dx)
            if 0 <= p1y < R and 0 <= p1x < C and G[p1y][p1x] != '#':
                candidates.append(p1)
        candidates += portals[G[py][px]]
        for p1 in candidates:
            if p1 not in visited:
                visited.add(p1)
                q.append((p1, d+1))
    return res


