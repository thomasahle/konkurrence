from typing import List
# Write any import statements here

def getMaxCollectableCoins(R: int, C: int, G: List[List[str]]) -> int:
    down = 0 # Best coming down from last row
    for r in range(R-1, -1, -1):
        # First solve the case of coming from the left
        if 'v' not in G[r]:
            right = [G[r].count('*')]*C
        else:
            right = [0]*C
            i = G[r].index('v')
            for j in range(C):
                c = (i-j) % C
                g = G[r][c]
                if g == 'v':  right[c] = down
                if g in '>.': right[c] = right[(c+1)%C]
                if g == '*':  right[c] = 1 + right[(c+1)%C]
        # Then solve the case of coming from above
        new_down = 0
        for c, g in enumerate(G[r]):
            if g == '*':  new_down = max(new_down, 1 + down)
            if g in '.v': new_down = max(new_down, down)
            if g == '>':  new_down = max(new_down, right[c])
        down = new_down
    return down

print(getMaxCollectableCoins(3, 4, '''
.***
**v>
.*..'''.strip().split()))
