from typing import List

def getMinimumDeflatedDiscCount(N: int, R: List[int]) -> int:
  R = R[::-1]
  prev = R[0]
  res = 0
  for r in R[1:]:
    if r >= prev:
      prev = prev-1
      res += 1
    else:
      prev = r
  if prev < 1:
    return -1
  return res
