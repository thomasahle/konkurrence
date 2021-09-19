from typing import List

def getMinProblemCount(N: int, S: List[int]) -> int:
  return max(S) // 2 + any(s & 1 for s in S)

