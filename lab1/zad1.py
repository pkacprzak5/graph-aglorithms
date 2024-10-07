from queue import PriorityQueue, Queue

from dimacs import *

s = 1
t = 2

def load_graph(name):
    V, L = loadWeightedGraph(name)
    G = [[] for _ in range(V + 1)]
    for x, y, w in L:
        G[x].append((y, -w))
        G[y].append((x, -w))
    return V, G

def changed_dijkstra(name):
    V, G = load_graph(name)
    odl = [float('inf') for _ in range(V+1)]
    q = PriorityQueue()
    q.put((-float('inf'), s))
    while not q.empty():
        cost, v = q.get()
        if v == t:
            return (-1) * cost
        for u, w in G[v]:
            if max(w, cost) < odl[u]:
                odl[u] = max(cost, w)
                q.put((max(cost, w), u))


def find(v, P):
    if P[v]!=v:
        P[v] = find(P[v], P)
    return P[v]

def union(x, y, P, R):
    x = find(x, P)
    y = find(y, P)
    if x == y:
        return False
    if R[x] < R[y]:
        x, y = y, x
    P[y] = x
    if R[x]==R[y]:
        R[x] += 1
    return True

def find_union(name):
    V, L = loadWeightedGraph(name)
    L.sort(key= lambda x: -x[2])
    P = [i for i in range(V+1)]
    R = [0 for _ in range(V+1)]
    for u, v, w in L:
        union(u, v, P, R)
        if find(s, P) == find(t, P):
            return w


def bfs(G, V, limit):
    q = Queue()
    q.put(s)
    visited = [False for _ in range(V+1)]
    visited[1] = True
    while not q.empty():
        v = q.get()
        if v == t:
            return True
        for u, weight in G[v]:
            weight *= (-1)
            if weight >= limit and not visited[u]:
                q.put(u)
                visited[u] = True

    return False


def bin_search(name):
    V, L = loadWeightedGraph(name)
    L.sort(key=lambda x : x[2])
    V, G = load_graph(name)
    p = 0
    k = len(L)-1
    while p < k:
        mid = (k+p)//2
        limit = L[mid][2]
        if bfs(G, V, L[mid][2]):
            p = mid+1
        else:
            k = mid-1

    if p == 0:
        return L[0][2]
    return L[p-1][2]

names = ['testy/clique5', 'testy/clique20', 'testy/clique100', 'testy/clique1000',
         'testy/g1', 'testy/grid5x5', 'testy/grid100x100', 'testy/path10',
         'testy/path1000', 'testy/path10000', 'testy/pp10', 'testy/pp100',
         'testy/pp1000', 'testy/rand20_100', 'testy/rand100_500',
         'testy/rand1000_100000']

i = 0
for name in names:
    # ans = changed_dijkstra(name)
    # ans = find_union(name)
    ans = bin_search(name)
    if ans == int(readSolution(name)):
        print("OK", i)
    else:
        print('Excpected: ', readSolution(name))
        print('Got: ', ans)
        print("WRONG", i)
    i += 1
