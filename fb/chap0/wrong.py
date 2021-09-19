
def getWrongAnswers(N: int, C: str) -> str:
  return ''.join({'A':'B','B':'A'}[c] for c in C)

