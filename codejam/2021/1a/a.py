import sys
read = lambda f=int: map(f, sys.stdin.readline().split())
array = lambda *ds: [array(*ds[1:]) for _ in range(ds[0])] if ds else 0

def l(x):
    return len(str(x))
def h(x, n):
    return int(str(x)[:n])

def solve(xs):
    res = 0
    last = xs[0]
    for x in xs[1:]:
        if last < x:
            last = x
        else:
            head = h(last, l(x))
            # If same head, we can just copy last
            # However, not if that changes the head.
            if l(last) > l(x) and head == x and h(last+1, l(x)) == head:
                res += l(last+1) - l(x)
                last = last + 1
            # Otherwise just add zeros
            elif head < x:
                zs = l(last) - l(x)
                res += zs
                last = x * 10**zs
            elif head >= x:
                zs = l(last) - l(x) + 1
                res += zs
                last = x * 10**zs
        #print(x, last)
    return res

T, = read()
for case in range(T):
    N, = read()
    xs = list(read())
    res = solve(xs)
    print(f'Case #{case+1}:', res)
