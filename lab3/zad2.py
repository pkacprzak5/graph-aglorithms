import os
from queue import PriorityQueue

from dimacs import *

class Node:
  def __init__(self):
    self.edges = {}

  def addEdge( self, to, weight):
    self.edges[to] = self.edges.get(to,0) + weight

  def delEdge( self, to ):
    del self.edges[to]


def load_graph(name):
    V, L = loadWeightedGraph(name)
    G = [Node() for i in range(V+1)]

    for (x, y, c) in L:
        G[x].addEdge(y, c)
        G[y].addEdge(x, c)

    return G, V


def merge_verices(G, x, y):
    G[x].delEdge(y)
    for v, weight in G[y].edges.items():
        if v == x:
            continue
        G[x].addEdge(v, weight)
        G[v].addEdge(x, weight)
        G[v].delEdge(y)

    G[y].edges = {}


def minimumCutPhase( G ):
    vs = 1
    for i in range(len(G)):
        if len(G[i].edges) > 0:
            vs = i
            break
    S = [vs]

    q = PriorityQueue()

    L = [0] * len(G)
    for u, weight in G[vs].edges.items():
        L[u] = weight
        q.put((-weight, u))


    while len(S) < 2:
        cost, v = q.get()
        if v in S:
            break
        S.append(v)
        for u, weight in G[v].edges.items():
            L[u] += weight
            q.put((-L[u], u))

    merge_verices(G, S[-1], S[-2])

    pot_wyn = L[S[-1]]
    return pot_wyn


def solve(name):
    G, V = load_graph(name)
    ans = float('inf')
    i = 0
    while i < len(G)-1:
        ans = min(ans, minimumCutPhase(G))
        i += 1

    return ans


folder_path = 'testy'
i = 0
for item in os.listdir(folder_path):
    name = os.path.join(folder_path, item)
    ans = solve(name)
    if ans == int(readSolution(name)):
        print("OK", i)
    else:
        print('Excpected: ', readSolution(name))
        print('Got: ', ans)
        print("WRONG", i)
    i += 1