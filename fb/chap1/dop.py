import itertools

def getArtisticPhotographCount(N: int, C: str, X: int, Y: int) -> int:
  res = 0
  for i, j, k in itertools.combinations(range(N), 3):
    if X <= abs(i-j) <= Y and X <= abs(j-k) <= Y \
        and C[i]+C[j]+C[k] in ('PAB', 'BAP'):
      res += 1
  return res

