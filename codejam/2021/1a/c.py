import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0
import itertools
from fractions import Fraction

def binom(n, k):
    if not 0 <= k <= n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
    for i in range(k):
        res //= (k - i)
    return res

def s2str(Q, s):
    return ''.join('TF'[int(i in s)] for i in range(Q))

def ham(Q, set1, set2):
    return len(set1 & set2) + len(set(range(Q)) - set1 - set2)

def bf(Q, exams, scores):
    w = [0]*Q
    denom = 0
    for trus in itertools.product(range(2), repeat=Q):
        tset = {i for i in range(Q) if trus[i]}
        if all(ham(Q, tset, e) == s for e, s in zip(exams, scores)):
            for i in tset:
                w[i] += 1
            denom += 1
    #print(f'{w=}')
    score = sum(max(wi,denom-wi)/denom for wi in w)
    #print(f'{score=}')


def solve(Q, exams, scores):
    N = len(exams)
    w = [0]*Q
    if N == 1:
        e, s = exams[0], scores[0]
        if s >= Q/2:
            return s2str(Q, e), 0
        return s2str(Q, set(range(Q))-s), 0
    if N == 2:
        e1, e2 = exams
        s1, s2 = scores
        sets = [e1&e2, e1-e2, e2-e1, set(range(Q))-e1-e2]
        a, b, c = len(e1&e2), len(e1-e2), len(e2-e1)
        d = Q - a - b - c
        denom = 0
        w = [0]*4
        #print(a, b, c, d)
        assert (s1+s2)%2==0
        for z in range(a+1):
            for x in range(b+1):
                t = (2*z+b+c+2*d-s1-s2)//2
                y = (2*x+c-b-(s1-s2))//2
                ways = binom(a, z) * binom(b, x) * binom(c, y) * binom(d, t)
                #print(f'{z=}, {x=}, {y=}, {t=}, {ways=}')
                if ways == 0:
                    continue
                denom += ways
                # In how many of the ways is the target coordinate included in the
                # given way?
                w[0] += ways * Fraction(z,a) if z else 0
                w[1] += ways * Fraction(x,b) if x else 0
                w[2] += ways * Fraction(y,c) if y else 0
                w[3] += ways * Fraction(t,d) if t else 0
        #print(f'{w=}, {denom=}')
        #print([len(s) for s in sets])
        res = 0
        guess = set()
        for i, s in enumerate(sets):
            if w[i] / denom >= 1/2:
                guess |= s
            res += len(s) * Fraction(max(denom-w[i], w[i]), denom)
        return ''.join('TF'[int(i in guess)] for i in range(Q)), res
    if N == 3:
        s1, s2, s3 = scores
        # a[1][0][0] is the number of question on which student 1 said YES
        # and student 2 and 3 said NO.
        subsets = array(2,2,2)
        a = array(2,2,2)
        for ii in itertools.product(range(2), repeat=3):
            theset = set(range(Q))
            for i, s in zip(ii, exams):
                if i == 1:
                    theset &= s
                else: theset -= s
            i, j, k= ii
            subsets[i][j][k] = theset
            a[i][j][k] = len(theset)
        #print(subsets)
        #print(a)
        c = array(2,2,2)
        w = array(2,2,2)
        denom = 0
        # Maybe this would be faster if we picked the smallest four regions
        # to use as a base for the iteration, but it should only save a factor 2^4
        # in the worst case.
        for c111, c000, c100, c101, c110 in itertools.product(
                range(a[1][1][1]+1),
                range(a[0][0][0]+1),
                range(a[1][0][0]+1),
                range(a[1][0][1]+1),
                range(a[1][1][0]+1)):
            c[1][1][1] = c111
            c[0][0][0] = c000
            c[1][0][0] = c100
            c[1][0][1] = c101
            c[1][1][0] = c110
            c[0][0][1] = (-s1 - s2 + 2*a[0][0][0] + 2*a[0][0][1] + a[0][1][0] + a[0][1][1] + a[1][0][0] + a[1][0][1] - 2*c[0][0][0] + 2*c[1][1][0] + 2*c[1][1][1])//2
            c[0][1][0] = (-s1 - s3 + 2*a[0][0][0] + a[0][0][1] + 2*a[0][1][0] + a[0][1][1] + a[1][0][0] + a[1][1][0] - 2*c[0][0][0] + 2*c[1][0][1] + 2*c[1][1][1])//2
            c[0][1][1] = (s2 + s3 - 2*a[0][0][0] - a[0][0][1] - a[0][1][0] - 2*a[1][0][0] - a[1][0][1] - a[1][1][0] + 2*c[0][0][0] + 2*c[1][0][0] - 2*c[1][1][1])//2
            if not all(0 <= c[i][j][k] <= a[i][j][k] for i, j, k in itertools.product(range(2), repeat=3)):
                continue
            ways = 1
            for i, j, k in itertools.product(range(2), repeat=3):
                ways *= binom(a[i][j][k], c[i][j][k])
            denom += ways
            #print('sum ways', sum(c[i][j][k] for i, j, k in itertools.product(range(2), repeat=3)))
            #print(a, c, ways)
            for i, j, k in itertools.product(range(2), repeat=3):
                w[i][j][k] += ways * Fraction(c[i][j][k], a[i][j][k]) if c[i][j][k] else 0
        print(f'{w=}')
        res = 0
        guess = set()
        #print(w)
        for i, j, k in itertools.product(range(2), repeat=3):
            s = subsets[i][j][k]
            # Somehow I have turned this upside down.
            #if 2*w[i][j][k] >= denom:
            if 2*w[i][j][k] <= denom:
                guess |= s
            res += len(s) * Fraction(max(denom-w[i][j][k], w[i][j][k]), denom)
        return ''.join('TF'[int(i in guess)] for i in range(Q)), res

    assert False




T, = read()
for case in range(T):
    N, Q = read()
    sets, scores = [], []
    for _ in range(N):
        answers, correct = read(str)
        sets.append(set(i for i in range(Q) if answers[i] == 'T'))
        scores.append(int(correct))
    while N != 3:
    #if N == 1:
        sets.append(sets[-1])
        scores.append(scores[-1])
        N += 1
    guess, res = solve(Q, sets, scores)
    #bf(Q, sets, scores)
    print(f'Case #{case+1}:', guess, f'{res.numerator}/{res.denominator}')
