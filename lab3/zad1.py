import os
from copy import deepcopy
from dimacs import *

def load_graph(name):
    V, L = loadWeightedGraph(name)
    M = [[-1] * (V + 1) for _ in range(V + 1)]
    for x, y, w in L:
        M[x][y] = 1
        M[y][x] = 1
    for i in range(1, V+1):
        for j in range(1, V+1):
            if M[i][j] != -1 and M[j][i] == -1:
                M[y][x] = 0

    return V, M

def dfs(G, v, t, visited):
    stack = []
    path = []
    min_flow = float('inf')
    stack.append((v, min_flow, path))
    while len(stack) > 0:
        v, min_flow, path = stack[-1]
        stack.pop()
        path.append(v)
        if v == t:
            return min_flow, path
        visited[v] = True

        for i in range(len(G)):
            if G[v][i] > 0 and not visited[i]:
                stack.append((i, min(min_flow, G[v][i]), path.copy()))


    return None, None

def notconnected(G, s, t, visited):
    stack = []
    stack.append(s)
    while len(stack) > 0:
        v = stack[-1]
        stack.pop()
        if v == t:
            return False
        visited[v] = True

        for i in range(len(G)):
            if G[v][i] > 0 and not visited[i]:
                stack.append(i)
    return True

def ford_fulk(name, fnc):
    V, G = load_graph(name)
    visited = [False] * (V+1)
    ans = float('inf')
    while fl is not None:
        ans = fl
        for i in range(len(path)-1):
            v = path[i]
            u = path[i+1]
            G[v][u] = 0
            if G[u][v] == -1:
                G[u][v] = 0
            G[u][v] = 0
        visited = [False] * (V + 1)
        fl, path = fnc(G, 1, V, visited)
    return ans


folder_path = 'testy'
i = 0
for item in os.listdir(folder_path):
    name = os.path.join(folder_path, item)
    ans = ford_fulk(name, dfs)
    if ans == int(readSolution(name)):
        print("OK", i)
    else:
        print('Excpected: ', readSolution(name))
        print('Got: ', ans)
        print("WRONG", i, name)
    i += 1