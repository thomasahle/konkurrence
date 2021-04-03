import sys
import random
n = int(sys.argv[1])
print(n)
for i in range(n):
    j = 0
    while random.random() < .5:
        j += 1
    print(j, end=' ')
print()
