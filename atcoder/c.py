import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

N, = read()
As = [1]*(N+1)
for i in range(2, N+1):
    if As[i] == 1: # Primes only
        pi = 1
        while pi*i <= N:
            pi *= i
            #print('Doing', pi)
            for j in range(pi, N+1, pi):
                As[j] += 1

#Bs = [0, 1]
#for i in range(2, N+1):
#    Bs.append(1)
#    while any(i%j==0 and Bs[j]==Bs[i] for j in range(1, i)):
#        Bs[i] += 1

print(' '.join(map(str,As[1:])))

#print(' '.join(map(str, As)))
#print([As[2*i] for i in range(1, N+1)])
#print(As[1:])
#print([1+sum(1 for j in range(2,i) if i%j==0 and not any(j%p==0 for p in range(2,j))) for i in range(1, N+1)])
