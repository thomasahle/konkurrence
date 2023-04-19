import random
T = 10
WS = 5
LEN = 3
alf = 'abcd'

print(T)
for _ in range(T):
    N = random.randrange(1, WS)
    print(N)
    for i in range(N):
        w = ''.join(random.choice(alf) for _ in range(LEN))
        print(w, end=' ')
    print()
