import sys
n = int(sys.argv[1])
import random
print(n)
xvs = []
M = 10**9
for _ in range(n):
    x = random.randrange(-M, M)
    v = random.randrange(-M, M)
    xvs.append((x,v))
xvs.sort()
for x, v in xvs:
    print(x, v)
