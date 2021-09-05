# Write any import statements here

def getArtisticPhotographCount(N: int, C: str, X: int, Y: int) -> int:
    return solveBAP(N, C, X, Y) + solveBAP(N, C[::-1], X, Y)

def solveBAP(N, C, X, Y):
    # b = Bs in [i-Y, i-X]
    b = 0
    # p = Ps in [i+X, i+Y]
    p = C[X-1:Y].count('P')
    #A..PP
    #print(p)
    res = 0
    for i, c in enumerate(C):
        if i-X >= 0 and C[i-X] == 'B': b += 1
        if i-Y-1 >= 0 and C[i-Y-1] == 'B': b -= 1
        if i+X-1 < N and C[i+X-1] == 'P': p -= 1
        if i+Y < N and C[i+Y] == 'P': p += 1
        #print(i, C[i], p, b)
        if c == 'A': res += b * p
    return res

import random, itertools
def bf(N, C, X, Y):
  res = 0
  for i, j, k in itertools.combinations(range(N), 3):
    if X <= abs(i-j) <= Y and X <= abs(j-k) <= Y \
        and C[i]+C[j]+C[k] in ('PAB', 'BAP'):
      res += 1
  return res

# j in [i+X, i+Y]
# means |i-j| = j-i \in [X, Y].

N = 10
C = ''.join(random.choice('.ABP') for _ in range(N))
#C = 'PAA.BAPAP.'
print(C)
print('real', getArtisticPhotographCount(N, C, 1, 1))
print('bf', bf(N, C, 1, 1))

