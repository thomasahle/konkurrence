from typing import List

import matplotlib.pyplot as plt

# H1/B*(D1+D2) + H2/B*D2 = (H1 D1 + H1 D2 + H2 D2)/B

def getMaxDamageDealt(N: int, H: List[int], D: List[int], B: int) -> float:
    # We ignore the issue of repeating the point as first.
    # Our new points are (H*D, D)
    # We sort by x/y, that is H.
    hds = sorted(zip(H, D))
    hdds = [(h*d,d) for h,d in hds]
    i1s = ghscan(hdds)
    p1s = [hdds[i] for i in i1s]
    # We make a second data structure for the next "layer" of points.
    s = set(i1s)
    inner = [i for i in range(N) if i not in s]
    if inner:
        i2s = ghscan([hdds[i] for i in inner])
        # Convert indices back to hdds space
        i2s = [inner[j] for j in i2s]
        p2s = [hdds[i] for i in i2s]
    else:
        i2s = None

    # Now use Graham scan to remove everything not on the hull...
    best = 0
    for i, (h1, d1) in enumerate(hds):
        #ideal0 = max(range(N), key=lambda k: ip((1,h1), hdds[k]))
        #ideal = max([k for k in range(N) if k != i],
                    #key=lambda k: ip((1,h1), hdds[k]))
        # find h2, d2 maximizing h2*d2 + h2*h1
        j1 = search(p1s, (1, h1))
        j = i1s[j1]
        #assert j == ideal0
        # If we get the same point back, we have to do some work
        # to find an alternative
        if i == j:
            #print(f'Need alternative {i=} {j=} {ideal0=} {ideal=}')
            candidates = []
            if j1-1 >= 0: candidates.append((i1s[j1-1], p1s[j1-1]))
            if j1+1 < len(i1s): candidates.append((i1s[j1+1], p1s[j1+1]))
            if i2s is not None:
                j = search(p2s, (1, h1))
                candidates.append((i2s[j], p2s[j]))
            j, _ = max(candidates, key=lambda i_p: ip((1,h1), i_p[1]))
            #assert j == ideal

        best = max(best, h1*d1 + h1*hdds[j][1] + hdds[j][0])

    return best/B

def ccw(o, p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2
    ox, oy = o
    return (p1x-ox)*(p2y-oy) - (p1y-oy)*(p2x-ox)

def ip(p1, p2):
    return p1[0]*p2[0] + p1[1]*p2[1]

def ghscan(ps):
    # Assumes this is sorted by y/x
    # ps.sort(key=lambda y/x)
    s = []
    for i, p in enumerate(ps):
        while len(s) > 1 and ccw(ps[s[-2]], ps[s[-1]], p) >= 0:
            s.pop()
        s.append(i)
    return s

def search(hull, x):
    l, r = 0, len(hull)-1
    while r - l > 2:
        m1 = (l+r)//2
        m2 = m1+1
        assert l < m1 < m2 < r
        if ip(hull[m1], x) > ip(hull[m2], x):
            r = m2
        else: l = m1
    return max(range(l, r+1), key=lambda i: ip(hull[i], x))

def test():
    import numpy as np
    xs = np.abs(np.random.randn(100,2))
    xs = xs[np.argsort(xs[:,0]/xs[:,1])]
    hull = [xs[i] for i in ghscan(xs)]
    i = search(hull, (1,1))
    j = max(range(len(xs)), key=lambda k: ip(xs[k], (1,1)))
    m = max(range(len(hull)), key=lambda k: ip(hull[k], (1,1)))
    print(i, j, m)
    print(hull[i], xs[j], hull[m])

    plt.scatter(*zip(*xs))
    plt.scatter(*zip(*hull))
    plt.show()

#test()

print(getMaxDamageDealt(3, [2,1,4], [3,1,2], 4))
print(getMaxDamageDealt(4, [1,1,2,100], [1,2,1,3], 8))
print(getMaxDamageDealt(4, [1,1,2,3], [1,2,1,100], 8))

# En anden løsning er at lave to dataset:
# (1, h, hd)
# (hd, d, 1)
# Og så finde det største indre produkt.
