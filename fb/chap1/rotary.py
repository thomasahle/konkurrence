from typing import List

def getMinCodeEntryTime(N: int, M: int, C: List[int]) -> int:
  C = [c-1 for c in C] # Let's 0 index
  res = 0
  prev = 0
  for c in C:
    res += min((prev-c)%N, (c-prev)%N)
    prev = c
  return res

