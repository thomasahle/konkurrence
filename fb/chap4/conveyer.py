# This code is from when I thought I had to set every conveyer belt,
# and not just one

from typing import List

def getMinExpectedHorizontalTravelDistance(
        N: int, H: List[int], A: List[int], B: List[int]) -> float:
    W = 1_000_000 # Width of space
    roots, G = make_graph(W, H, A, B)
    print('Roots:', roots)
    print('Graph:')
    for g in G:
        print(g)
    res = 0
    for (i, p, w) in roots:
        dists = bfs(G, i, p)
        print(f'Root({i=}, {p=}, {w=})')
        for p, h in sorted(dists.items()):
            print(f'dist to {p} is {h}')
        minh = min(dists.values())
        res += w * minh
    return res / W


from collections import deque
def bfs(G, root, pos):
    node = (root, pos, 0)
    #seen = {node} # Not needed, since I can only go each place in one way
    # Actually we could see the same position in multiple ways, if we have
    # one belt subsuming another belt...
    q = deque()
    q.append(node)
    dists = {}
    while q:
        i, p, h = q.popleft()
        if i == len(G)-1:
            dists[p] = h
            continue
        (i1, p1), (i2, p2) = G[i]
        assert p1 < p < p2, f'{p1=} {p=} {p2=}'
        q.append((i1, p1, h+p-p1))
        q.append((i2, p2, h+p2-p))
    return dists


def make_graph(W, H, A, B):
    # We can make a list of up to N top-nodes, which represent where packages
    # can land, including weight.

    # We handle END before START to avoid end-point captures
    # If a package lands _strictly_ within conveyor belt i
    # (excluding its endpoints), then it will be transported
    # to its left or right end
    START, END = 1, 0
    events = [(a, START, i) for i, a in enumerate(A)]
    events += [(b, END, i) for i, b in enumerate(B)]
    events.sort()

    #fw = SegmentTree(2**20) # NOTE: must be larger than the max height
    fw = SegmentTreeBrute()
    G = [([0, 0], [0, 0]) for _ in range(len(H)+1)]
    roots = []
    top_envelope_start = 0
    top_envelope_i = len(H)
    fw.add(len(H), 0) # Add the bottom
    for p, typ, i in events:
        if typ == START:
            #fw.add(H[i], i)
            G[i][0][0] = fw.next(-H[i])
            G[i][0][1] = p
            fw.add(i, -H[i])
            # if i is the top it covers something else and starts a new root
            if fw.top() == i:
                roots.append((top_envelope_i, (top_envelope_start+p)/2, p-top_envelope_start))
                top_envelope_i = i
                top_envelope_start = p
        if typ == END:
            G[i][1][0] = fw.next(-H[i])
            G[i][1][1] = p
            fw.remove(i)
            if top_envelope_i == i:
                roots.append((i, (top_envelope_start+p)/2, p-top_envelope_start))
                top_envelope_i = fw.top()
                top_envelope_start = p
    assert top_envelope_i == len(H)
    roots.append((len(H), (top_envelope_start+W)/2, W-top_envelope_start))
    return roots, G


class SegmentTreeBrute:
    def __init__(self):
        self.data = {}
    def add(self, k, v):
        self.data[k] = v
    def remove(self, k):
        del self.data[k]
    def next(self, v):
        v0, k = min((v0, k) for k, v0 in self.data.items() if v0 > v)
        return k
    def top(self):
        return self.next(-10**9)



class SegmentTree:
    def __init_(self, size):
        h = size.bit_length
        assert size == 1 << h-1, 'Size must be power of 2'
    def next(self, v):
        # Return first k,v' with v' > v
        return first




def test_cases():
    N = 2
    H = [10, 20]
    A = [100000, 400000]
    B = [600000, 800000]
    print(getMinExpectedHorizontalTravelDistance(N, H, A, B))

    N = 5
    H = [2, 8, 5, 9, 4]
    A = [5000, 2000, 7000, 9000, 0]
    B = [7000, 8000, 11000, 11000, 4000]
    print(getMinExpectedHorizontalTravelDistance(N, H, A, B))
test_cases()
