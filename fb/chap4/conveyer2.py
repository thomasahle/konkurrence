from typing import List

# You solved 7 / 19 test cases.
# Time Limit Exceeded on 7 test cases
# Wrong Answer on 5 test cases

def getMinExpectedHorizontalTravelDistance(
        N: int, H: List[int], A: List[int], B: List[int]) -> float:
    W = 1_000_000 # Width of space
    roots, G = make_graph(W, H, A, B)
    pss, prices = push_down(G, roots, A, B)

    # print_graph(G, A, B, H)

    expectation = 0
    for i, ps in enumerate(pss[:-1]):
        expectation += (B[i]-A[i])/2 * sum(w for _, w in ps)

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
    for i, ((i1, _), (i2, p)) in enumerate(G[:-1]):
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
    order = topsort(G)

    # All incoming positions and their probabilities when
    # conveyer belts are chosen at random.
    pss = [[] for _ in G]
    # Start by adding roots
    for (i, p, w) in roots:
        pss[i].append((p, w))
    # Go through graph in topological order,
    # ignore the bottom.
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
    events = [(a, START, -H[i], i) for i, a in enumerate(A)]
    events += [(b, END, H[i], i) for i, b in enumerate(B)]
    events.sort()

    fw = KeyedSegmentTree(2**20) # NOTE: must be larger than the max height
    MH = 10**6 # Add this value to all height to make them positive before putting in tree
    #fw = SegmentTreeBrute()
    G = [[(None, 0), (None, 0)] for _ in range(len(H)+1)]
    roots = []
    top_envelope_start = 0
    top_envelope_i = len(H)
    fw.add(len(H), MH+0) # Add the bottom
    #to_add = [] # Starts we haven't added yet to prevent accidential catching
    for p, typ, _, i in events:
        if typ == START:
            G[i][0] = (fw.next(MH-H[i]), p)
            fw.add(i, MH-H[i])
            # if i is the top it covers something else and starts a new root
            if fw.top() == i:
                roots.append((top_envelope_i, (top_envelope_start+p)/2, p-top_envelope_start))
                top_envelope_i = i
                top_envelope_start = p
        if typ == END:
            G[i][1] = (fw.next(MH-H[i]), p)
            fw.remove(i)
            if top_envelope_i == i:
                roots.append((i, (top_envelope_start+p)/2, p-top_envelope_start))
                top_envelope_i = fw.top()
                top_envelope_start = p
    assert top_envelope_i == len(H)
    roots.append((len(H), (top_envelope_start+W)/2, W-top_envelope_start))
    return roots, G

def print_graph(G, A, B, H):
    # For debugging the make_graph

    from graphviz import Digraph

    dot = Digraph()
    for i, ((i1, _), (i2, _)) in enumerate(G):
        if i == len(G)-1:
            dot.node(str(i), 'bot')
        else:
            dot.node(str(i), f'{H[i]}: {A[i]}-{B[i]}' if i != len(G)-1 else 'bot')
            dot.edge(str(i), str(i1))
            dot.edge(str(i), str(i2))

    dot.render(view=True)



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
        v0, k = min((v0, k) for k, v0 in self.data.items())
        return k

################################################################################
# The following recursive tree uses way too much memory unfortunately.
################################################################################

class Branch:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.size + right.size
        self.update()

    def set(self, i, v):
        left, right = self.left, self.right
        if i < left.size:
            left.set(i, v)
        else:
            right.set(i-left.size, v)
        self.update()

    def update(self):
        left, right = self.left, self.right
        if left.last is None and right.last is None:
            self.last = None
        elif right.last is not None:
            self.last = right.last + left.size
        else:
            self.last = left.last

    def succ(self, i):
        left, right = self.left, self.right
        if left.last is not None and left.last > i:
            return left.succ(i)
        #assert right.last is not None and right.last > i-left.size, f'{right.last=}, {i=}, {left.size=}'
        return right.succ(i - left.size) + left.size

class Leaf:
    def __init__(self):
        self.size = 1
        self.last = None

    def set(self, i, v):
        assert i == 0
        self.last = 0 if v > 0 else None

    def succ(self, i):
        assert i < 0 and self.last is not None
        return 0

def Tree(size):
    h = size.bit_length()
    assert size == 1 << h-1, 'Size must be power of 2'

    if size == 1:
        return Leaf()
    return Branch(Tree(size//2), Tree(size//2))

class RecursiveTree:
    def __init__(self, size):
        self.t = Tree(size)
        self.v2k = {}
        self.k2v = {}
    def add(self, k, v):
        #print('Adding', v)
        self.t.set(v, 1)
        #print('New last', self.t.last)
        self.v2k[v] = k
        self.k2v[k] = v
    def remove(self, k):
        v = self.k2v.pop(k)
        del self.v2k[v]
        #print('Removing', v)
        self.t.set(v, 0)
    def next(self, v):
        #print('Getting successor for', v)
        v1 = self.t.succ(v)
        #print('Found', v1)
        return self.v2k[v1]
    def top(self):
        return self.next(-1)


################################################################################
# Let's try a real Segment tree
################################################################################

class SegmentTree:
    def __init__(self, size):
        h = size.bit_length()
        assert size == 1 << h-1, 'Size must be power of 2'
        self.h = h
        self.last = [-1] * (1 << h)
        # Recall, children of i are 2i+1 and 2i+2
        # The parent of i is (i-1) >> 1
        # That makes the parent of 0 = (-1)>>1 = -1
        # Three tree at i has size 2**(h - (i+1).bit_length())

    def set(self, i, v):
        p = (1 << self.h-1) - 1 + i
        self.last[p] = 0 if v != 0 else -1
        p = (p-1) >> 1
        while p != -1:
            l, r = self.last[2*p+1], self.last[2*p+2]
            if l == -1 and r == -1:
                self.last[p] = -1
            elif r != -1:
                left_size = 1 << (self.h - (2*p+2).bit_length())
                self.last[p] = r + left_size
            else:
                self.last[p] = l
            p = (p-1) >> 1

    def succ(self, i):
        p = 0
        res = 0
        for _ in range(self.h-1):
            l, r = self.last[2*p+1], self.last[2*p+2]
            if l != -1 and l > i:
                p = 2*p+1
            else:
                left_size = 1 << (self.h - (2*p+2).bit_length())
                i -= left_size
                res += left_size
                p = 2*p+2
        return res

class KeyedSegmentTree:
    def __init__(self, size):
        self.t = SegmentTree(size)
        self.v2k = {}
        self.k2v = {}
    def add(self, k, v):
        #print('Adding', v)
        self.t.set(v, 1)
        #print('New last', self.t.last[0])
        self.v2k[v] = k
        self.k2v[k] = v
    def remove(self, k):
        v = self.k2v.pop(k)
        del self.v2k[v]
        #print('Removing', v)
        self.t.set(v, 0)
    def next(self, v):
        #print('Getting successor for', v)
        v1 = self.t.succ(v)
        #print('Found', v1)
        return self.v2k[v1]
    def top(self):
        return self.next(-1)







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
