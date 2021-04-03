import sys
n = int(sys.argv[1])
import random
print(n)
print(' '.join(map(str, (random.randrange(-10,10) for _ in range(n)))))
