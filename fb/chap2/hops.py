from typing import List

# Strategy:
# train = ...
# find next frog,
# move train up to frog
# then add frog to train

def getSecondsRequired(N: int, F: int, P: List[int]) -> int:
    P.sort()
    p = 0 # Train start position
    ts = 0 # Train size
    for i, p in enumerate(P):
        if i == p:
            ts += 1
        else:
            break

    res = 0
    # While all frogs are not in the train
    while ts != F:
        j = P[ts] # Position of next train
        s = j - p - ts # Steps to move train
        res += s
        p += s
        ts += 1

    res += N - p
    return res





