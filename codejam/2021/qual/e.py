import sys
from itertools import groupby
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0
from math import log, exp
import random

def inv(v):
    # Decreasing, higher p -> smaller difficulty
    if v < 0.115112: return 3
    if v > 1-0.115112: return -3
    return log(-((-exp(6) + exp(6*v))/(exp(3)*(-1 + exp(6*v)))))

# p = sigmoid(S-Q)
def sigmoid(x):
    return 1/(1 + exp(-x))

def solve(X):
    N, M = len(X), len(X[0])
    qs = [inv(sum(col)/N) for col in zip(*X)]
    #skills = []
    besti, bestb = 0, 0
    for i in range(N):
        v1 = sum(X[i])/M # Assuming didn't cheat
        if v1 < 1/2:
            continue
        v2 = 2*v1-1      # Assuming did cheat
        s1 = inv(1-v1)   # Because inv is inversed for s
        s2 = inv(1-v2)
        bce1, bce2 = 0, 0
        for r, q in zip(X[i], qs):
            p1 = sigmoid(s1-q)
            p2 = (sigmoid(s2-q)+1)/2
            if r == 1:
                bce1 += log(1/p1)
                bce2 += log(1/p2)
            else:
                bce1 += log(1/(1-p1))
                bce2 += log(1/(1-p2))
        #print(i+1, bce1, bce2, bce1-bce2)
        # Loss with hypothesis 1 - loss with hyp 2.
        # Should be big if hyp 2 is more likely
        dif = bce1 - bce2
        if dif > bestb:
            besti, bestb = i, dif
    return besti

def test(N, M):
    ss = [random.random()*6-3 for _ in range(N)]
    qs = [random.random()*6-3 for _ in range(M)]
    X = [[int(random.random() < sigmoid(s-q)) for q in qs] for s in ss]
    c = random.randrange(N)
    for i in range(M):
        if random.random() < .5:
            X[c][i] = 1
    g = solve(X)
    return c == g

def local_main():
    N, M = 100, 10000
    reps = 100
    res = sum(test(N,M) for _ in range(reps))/reps
    print(res)

def main():
    T, = read()
    _P, = read()
    N = 100
    for case in range(T):
        X = []
        for _ in range(N):
            X.append(list(map(int,sys.stdin.readline()[:-1])))
        res = solve(X) + 1
        print(f'Case #{case+1}:', res)

local_main()
#main()
