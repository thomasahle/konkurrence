
def getSecondsElapsed(C, _N, A, B, K):
    # First handle full loops
    loop_ttime = sum(b-a for a,b in zip(A,B))
    res = C * (K // loop_ttime)
    K %= loop_ttime

    # If we finish right after the last tunnel
    if K == 0:
        return res - C + max(B)

    #print(f'{loop_ttime=}, {res=}, {K=}')
    # Then handle remainding
    for a, b in sorted(zip(A, B)):
        if b-a < K:
            K -= b-a
        else:
            end = a + K
            break
    res += end
    return res


print(getSecondsElapsed(10, 2, [1,6], [3,7], 7))
print(getSecondsElapsed(50, 3, [39,19,28], [49,27,35], 15))
