import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

sys.stderr.write = lambda w: None

from collections import defaultdict, Counter

# AAAACCCC
# AAADDDD

import itertools
def chunk(w):
    it = itertools.groupby(w)
    next(it)
    for c, _ in it:
        yield c


def solve(ws):
    plains = Counter()
    doubles = {}
    for w in ws:
        if len(set(w)) == 1:
            plains[w[0]] += len(w)
        else:
            # Only one edge out from each node
            if w[0] in doubles:
                print('Double edge', file=sys.stderr)
                return None
            # No self-loops
            #for c in list(chunk(w):
                #if c == w[0]:
                    #print('Self loop', file=sys.stderr)
                    #return None
            doubles[w[0]] = w

    for c, _ in plains.items():
        if any(c in list(chunk(w))[:-1] for w in doubles.values()):
            print(c, 'in the middle of other double', file=sys.stderr)
            return None

    roots = [c for c in doubles.keys()
            if not any(w2[-1] == c for w2 in doubles.values())]

    if doubles and not roots:
        print('Loop', file=sys.stderr)
        return None

    #print(roots)
    #print(plains)
    #print(doubles)

    dvis = set()

    visited = set()
    res = []
    for c in roots:
        if c in visited:
            print('Root seen', c, file=sys.stderr)
            return None
        cur = c
        while True:
            # Take all the trivial words at that location
            res.append(cur * plains[cur])
            # See if there is a next word we can visit in the chain?
            w = doubles.get(cur)
            if w is None:
                visited.add(cur)
                break
            dvis.add(cur)
            res.append(w)
            # Mark everything inside the word
            for c in chunk(w):
                if c in visited:
                    print('Already seen', c, file=sys.stderr)
                    return None
                visited.add(c)
                visited.add(cur)
            cur = w[-1]

    for c, i in plains.items():
        if c not in visited:
            res.append(c * i)
            visited.add(c)

    # See if there is anything left in doubles we haven't used
    for c in doubles:
        if c not in dvis:
            print('Leftovers', file=sys.stderr)
            return None

    return ''.join(res)



import itertools
def allchunk(w):
    it = itertools.groupby(w)
    for c, _ in it:
        yield c

def test(perm):
    seen = set()
    for c in allchunk(''.join(perm)):
        if c in seen:
            return False
        seen.add(c)
    return True

def brute(ws):
    any_res = False
    for perm in itertools.permutations(ws):
        if test(perm):
            any_res = True
            yield ''.join(perm)
    if not any_res:
        yield None

if False:
    import random
    while True:
        alf = 'abcd'
        n = random.randrange(1, 5)
        ws = []
        for i in range(n):
            w = ''.join(random.choice(alf) for _ in range(4))
            ws.append(w)

        ans = solve(ws)
        if not ans in brute(ws):
            print('Error', ans)
            print(ws)
            print(next(brute(ws)))
            break


T, = read()
for case in range(T):
    N, = read()
    xs = list(read(str))
    res = solve(xs)
    if res is None:
        res = 'IMPOSSIBLE'
    print(f'Case #{case+1}:', res)

