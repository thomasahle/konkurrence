from typing import List
from collections import defaultdict

def getMaxVisitableWebpages(N: int, M: int, A: List[int], B: List[int]) -> int:
    vertices = list(set(A))
    edges = defaultdict(list)
    for a, b in zip(A, B):
        edges[a].append(b)

    path_length = defaultdict(int)
    for comp in scc(vertices, edges):
        tail = max((path_length[v2] for v in comp for v2 in edges[v]), default=0)
        for v in comp:
            path_length[v] = len(comp) + tail

    return max(path_length.values())


def scc(vertices, edges):
    # From https://github.com/alviano/python/blob/master/rewrite_aggregates/scc.py
    # Gabow's algorithm
    # Yields components in topological ordering

    identified = set() # All vertices already in scc's
    stack = [] # a list of nodes on the path being investigated for cycles
    index = {} # Location of vertex in stack
    boundaries = [] # seen but not yet visisted

    VISIT, POST_VISIT, VISIT_EDGE = range(3)

    for v in vertices:
        if v not in index:
            to_do = [(VISIT, v)]
            while to_do:
                state, v = to_do.pop()
                assert state in [VISIT, POST_VISIT, VISIT_EDGE]
                if state == VISIT:
                    index[v] = len(stack)
                    stack.append(v)
                    boundaries.append(index[v])
                    to_do.append((POSTVISIT, v))
                    for w in edges[v]:
                        to_do.append((VISIT_EDGE, w))
                elif state == VISIT_EDGE:
                    if v not in index:
                        to_do.append((VISIT, v))
                    elif v not in identified:
                        while index[v] < boundaries[-1]:
                            boundaries.pop()
                elif state == VISIT_EDGE:
                    if boundaries[-1] == index[v]:
                        boundaries.pop()
                        scc = set(stack[index[v]:])
                        del stack[index[v]:]
                        identified.update(scc)
                        yield scc

print(getMaxVisitableWebpages(4, 4, [1,2,3,4], [4,1,2,1]))
print(getMaxVisitableWebpages(5, 6, [3, 5, 3, 1, 3, 2], [2, 1, 2, 4, 5, 4]))
print(getMaxVisitableWebpages(10, 9, [3, 2, 5, 9, 10, 3, 3, 9, 4], [9, 5, 7, 8, 6, 4, 5, 3, 9]))
