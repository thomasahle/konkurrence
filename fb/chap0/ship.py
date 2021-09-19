from typing import List

def getHitProbability(R: int, C: int, G: List[List[int]]) -> float:
  return sum(x for row in G for x in row)/(R*C)

