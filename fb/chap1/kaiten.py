from typing import List
from collections import Counter, deque

def getMaximumEatenDishCount(N: int, D: List[int], K: int) -> int:
  cnt = Counter()
  q = deque()
  res = 0
  for i, d in enumerate(D):
    if cnt[d] == 0:
      res += 1
      cnt[d] += 1
      q.append(d)
    if len(q) == K+1:
      d2 = q.popleft()
      cnt[d2] -= 1
  return res

