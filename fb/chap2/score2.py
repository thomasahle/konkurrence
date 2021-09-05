
def getMinProblemCount(N, S):
    res = max(S)
    for ones in [0,1]:
        for twos in [0,1,2]:
            m = max(S) // 3
            for threes in [m, m-1, m-2]:
                if threes >= 0:
                    if all(test(s, ones, twos, threes) for s in S):
                        res = min(res, ones+twos+threes)
    return res

def test(s, ones, twos, threes):
    for i in range(ones+1):
        for j in range(twos+1):
            sr = s - (i + 2*j)
            if sr >= 0 and sr % 3 == 0 and sr//3 <= threes:
                return True
    return False


print(getMinProblemCount(5, [1,2,3,4,5]))
print(getMinProblemCount(4, [4,3,3,4]))
print(getMinProblemCount(4, [2,4,6,8]))
print(getMinProblemCount(1, [8]))
print(getMinProblemCount(5, [2,4,7,10,13]))
