import sys
import numpy as np
M = int(sys.argv[1])
ps = [p for p in range(2, 500) if all(p%q != 0 for q in range(2,p))]
print(1)
print(M)
w, i, j = 0, 0, 0
while i != M:
    n = np.random.poisson(2)
    if n != 0:
        #prob.append((ps[i], n))
        print(ps[j], n)
        w += n
        j += 1
    i += 1
#print(w)
#for p, n in prob:
    #print(p, n)


