def getMinCodeEntryTime(N, M, C):
    C = [1] + C
    M = len(C)
    dp = [0]*M
    for i in range(M-2, -1, -1):
        new = [0]*M
        for j in range(M):
            new[j] = min(r(C[i],C[i+1],N) + dp[j],
                         r(C[j],C[i+1],N) + dp[i])
        dp = new
    return dp[0]

def r(c1, c2, N):
    return min((c1-c2)%N, (c2-c1)%N)

def solve(i, j, C, N):
    # i is the position we just did
    # as well as the position of the last lock we changed.
    # j is the position (from C) of the other lock.
    if i == len(C)-1: return 0
    return min(r(C[i],C[i+1],N) + solve(i+1, j, C,N),
               r(C[j],C[i+1],N) + solve(i+1, i, C,N))

print(solve(0, 0, [1,1,2,3], 3))
print(solve(0, 0, [1,9,4,4,8], 10))
print(getMinCodeEntryTime(3, 3, [1,2,3]))
print(getMinCodeEntryTime(10, 4, [9,4,4,8]))
