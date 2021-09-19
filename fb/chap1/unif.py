def getUniformIntegerCountInInterval(A: int, B: int) -> int:
  res = 0
  for d in range(1,13):
    for c in range(10):
      i = int(str(c)*d)
      if A <= i <= B:
        res += 1
  return res

