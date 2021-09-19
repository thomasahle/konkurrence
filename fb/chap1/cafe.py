from typing import List

def getMaxAdditionalDinersCount(N: int, K: int, M: int, S: List[int]) -> int:
  S.sort()
  res = 0
  for s, t in zip([-K]+S, S+[N+K+1]):
    res += (t - s) // (K + 1) - 1
  return res

