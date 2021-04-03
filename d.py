from math import sqrt


cache = {}


def get_dist_sq(x, y):
    if (x, y) in cache:
        return cache[x, y]
    print(x, y, flush=True)
    cache[x, y] = int(input().strip())
    return cache[x, y]


def calc_dist_sq(pos0, pos1):
    x0, y0 = pos0
    x1, y1 = pos1
    return (x1 - x0) ** 2 + (y1 - y0) ** 2


def clip_pos(pos):
    x, y = pos
    x = min(max(x, 0), 10**6)
    y = min(max(y, 0), 10**6)
    return x, y
    


def find_ball(x0, y0):
    d2 = get_dist_sq(x0, y0)
    d = int(sqrt(d2))
    if d2 > 50:
        other_pos = [
            (x0 - d // 2, y0),
            (x0 + d // 2, y0),
            (x0, y0 - d // 2),
            (x0, y0 + d // 2),
        ]
        other_pos = list(map(clip_pos, other_pos))
        new_pos = min(other_pos, key=lambda pos: get_dist_sq(*pos))
        find_ball(*new_pos)
        return

    for x in range(x0 - d - 5, x0 + d + 5):
        for y in range(y0 - d - 5, y0 + d + 5):
            x, y = clip_pos((x, y))
            if calc_dist_sq((x0, y0), (x, y)) == d2:
                if get_dist_sq(x, y) == 0:
                    return

    assert False


def main():
    global cache
    n = int(input())
    for _ in range(n):
        cache = {}
        find_ball(0, 0)

main()