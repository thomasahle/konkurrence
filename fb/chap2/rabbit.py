def getMaxVisitableWebpages(N, L):
    L = [l-1 for l in L] # 0-index
    visited = [-1 for _ in range(N)]
    length = [0 for _ in range(N)]
    stack = []
    onstack = [False] * N
    def dfs(time, i):
        while not onstack[i] and not length[i]:
            stack.append(i)
            onstack[i] = True
            visited[i] = time
            time += 1
            i = L[i]

        # length[i] is only sat if this is a later dfs run and we are
        # discovering old information
        if not length[i]:
            # Everything in the loop gets the same 'length'
            #print(f'Rediscovered {i} at time {time}. First visited {visited[i]}')
            i0 = i
            length[i0] = time-visited[i0]
            while onstack[i0]:
                length[i] = length[i0]
                i = stack.pop()
                onstack[i] = False

        # Everything else gets 'one more'
        while stack:
            i1 = stack.pop()
            length[i1] = length[i] + 1
            onstack[i1] = False
            i = i1

    for i in range(N):
        #print(f'dfs(0, {i})')
        dfs(0, i)
        #print(visited, length)

    #print(visited, length)
    return max(length)

print(getMaxVisitableWebpages(4, [4,1,2,1]))
print(getMaxVisitableWebpages(4, [1,2,3,4]))
print(getMaxVisitableWebpages(4, [2,3,4,1]))
import itertools
for p in itertools.permutations([1,2,3,4]):
    print(p, getMaxVisitableWebpages(4, p))

