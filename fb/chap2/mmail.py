from typing import List
# Write any import statements here

# This solution is wrong because it assumes we know the current state of the
# warehouse once we have to make the decision.
def getMaxExpectedProfit(N: int, V: List[int], C: int, S: float) -> float:
    # We can "compress" the state space (Petrs words) by
    # noting that `val` is known once we know the last "steal time".
    def solve(val, i):
        if i == N:
            return 0
        val += V[i]
        opt1 = val - C + solve(0, i+1)
        opt2 = (1-S)*solve(val, i+1) + S*solve(0, i+1)
        return max(opt1, opt2)
    return solve(0, 0)



def getMaxExpectedProfit(N: int, V: List[int], C: int, S: float) -> float:
    def solve(ex_val, i):
        if i == N:
            return 0
        ex_val += V[i]
        opt1 = ex_val - C + solve(0, i+1)
        opt2 = solve(ex_val*(1-S), i+1)
        return max(opt1, opt2)
    return solve(0, 0)


import functools
def getMaxExpectedProfit(N: int, V: List[int], C: int, S: float) -> float:
    @functools.lru_cache(10**6)
    def solve(last_clear, i):
        if i == N:
            return 0
        ex_val = 0
        for j in range(last_clear+1, i+1):
            ex_val = ex_val*(1-S) + V[j]
        opt1 = ex_val - C + solve(i, i+1)
        opt2 = solve(last_clear, i+1)
        return max(opt1, opt2)
    return solve(-1, 0)


def getMaxExpectedProfit(N: int, V: List[int], C: int, S: float) -> float:
    evs = [0] # evs[i] = sum_{0 <= j < i} v[j]*(1-S)^{i-j-1}
    for v in V:
        evs.append(evs[-1]*(1-S) + v)
    #print(evs)
    def solve(last_clear, i):
        if i == N:
            return 0
        ex_val = evs[i+1] - evs[last_clear]*(1-S)**(i-last_clear+1)
        #old = 0
        #for j in range(last_clear+1, i+1):
            #old = old*(1-S) + V[j]
        #assert ex_val == old, (ex_val, old)
        opt1 = ex_val - C + solve(i+1, i+1)
        opt2 = solve(last_clear, i+1)
        return max(opt1, opt2)
    return solve(0, 0)



def getMaxExpectedProfit(N: int, V: List[int], C: int, S: float) -> float:
    evs = [0] # evs[i] = sum_{0 <= j < i} v[j]*(1-S)^{i-j-1}
    for v in V:
        evs.append(evs[-1]*(1-S) + v)
    dp = [0]*(N+1)
    for i in range(N-1, -1, -1):
        new = [0]*(N+1)
        for last_clear in range(i+1):
            ex_val = evs[i+1] - evs[last_clear]*(1-S)**(i-last_clear+1)
            new[last_clear] = max(ex_val - C + dp[i+1], dp[last_clear])
        dp = new
    return dp[0]

print(getMaxExpectedProfit(5, [10,2,8,6,4], 3, .15))





# Hvis jeg siger nej, betaler jeg i princippet S*den nuværende værdi.
# Så jeg kan bare se hvad der mest værd.
# Men! Når jeg har valgt ved jeg om pakken faktisk bliver stjået, så jeg skal gøre lidt mere.
# I øvrigt kan jeg ikke bare vælge greedy, for i det tilfælde hvor S=0, skal jeg altid vente indtil tilsidst.
