from typing import List

def getMinExpectedHorizontalTravelDistance(
        N: int, H: List[int], A: List[int], B: List[int]) -> float:
    W = 1_000_000 # Width of space
    roots, G = make_graph(W, H, A, B)
    pss, prices = push_down(G, roots, A, B)

    # for i in range(N+1):
    #     if i == N:
    #         print(f'bottom')
    #     else:
    #         print(f'{i}: {A[i]}-{B[i]} at H={H[i]}')
    #     for p, w in pss[i]:
    #         print(f'{p=}, {w/W=}')
    # print('Total bottom prob:', sum(w for _,w in pss[-1])/W)

    # expectation = 0
    # for i, ps in enumerate(pss):
    #     a, b = A[i], B[i]
    #     left = sum((p-a)*w for p, w in ps)
    #     right = sum((b-p)*w for p, w in ps)
    #     expectation += (left + right)/2
    # That could be made much easier, ignoring all the positions.
    expectation = 0
    for i, ps in enumerate(pss[:-1]):
        expectation += (B[i]-A[i])/2 * sum(w for _, w in ps)

    #print('All random cost:', expectation/W)
    #print(prices)

    # We can always do at least as well as random (MOCP)
    best = expectation
    for i, ps in enumerate(pss[:-1]):
        # Now what happens if we force this belt left or right?
        # It means something to the time on the belt itself,
        # but we also need to know the expected time the package
        # travels after falling off the left and right side
        # respectively.
        a, b = A[i], B[i]
        left = sum((p-a)*w for p, w in ps)
        right = sum((b-p)*w for p, w in ps)

        totw = sum(w for _, w in ps)
        (i1, _), (i2, _) = G[i]
        price_left, price_right = prices[i1], prices[i2]
        #print(f'{i=}, {price_left=}, {price_right=}, {left/W=}, {right/W=}')

        val = expectation \
                - (B[i]-A[i] + price_left + price_right)/2 * totw \
                + min(left+price_left*totw, right+price_right*totw)
        #print(i, f'{A[i]}-{B[i]}, H={H[i]}', 'cost', val/W)
        #if val < best:
            #print('Best', i, f'{A[i]}-{B[i]}, H={H[i]}')
        best = min(best, val)

    return best/W

def topsort(G):
    in_graph = [[] for _ in G]
    for i, ((i1, _), (i2, p)) in enumerate(G):
        in_graph[i1].append(i)
        in_graph[i2].append(i)

    outs = [2] * (len(G)-1) + [0]
    ready = [len(G)-1]
    res = []
    while ready:
        i = ready.pop()
        res.append(i)
        for i1 in in_graph[i]:
            outs[i1] -= 1
            if outs[i1] == 0:
                ready.append(i1)

    return res

def push_down(G, roots, A, B):
    # All incoming positions and their probabilities when
    # conveyer belts are chosen at random.
    pss = [[] for _ in G]
    # Start by adding roots
    for (i, p, w) in roots:
        pss[i].append((p, w))

    # Go through graph in topological order,
    # ignore the bottom.
    order = topsort(G)
    for i in order[:0:-1]:
        W = sum(w for _, w in pss[i])
        (i1, p1), (i2, p2) = G[i]
        pss[i1].append((p1, W/2))
        pss[i2].append((p2, W/2))

    # Also compute prices, going the other way through the order
    # This is the expected price a package will pay when landing
    # (anywhere) on the conveyer belt
    prices = [0]*len(G)
    # Again, skip the bottom. The bottom is free.
    for i in order[1:]:
        (i1, _), (i2, _) = G[i]
        prices[i] = (B[i]-A[i])/2 + (prices[i1] + prices[i2])/2

    return pss, prices

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
