from random import *
from cpgen.basic import *

# Generate a random unweighted tree
def Tree(N):
    edges = []
    for u in range(2, N + 1):
        v = randrange(1, u)
        edges.append([u, v])

    permutation = Permutation(N)

    for i in range(0, N - 1):
        u, v = edges[i]
        u = permutation[u - 1]
        v = permutation[v - 1]
        edges[i] = (u, v)
    return edges;


# Generate a random weighted tree
def WTree(N, L, R):
    weigths = Array(N - 1, L, R)
    tree = Tree(N)
    wtree = []

    for i in range(0, N - 1):
        u, v, w = tree[i][0], tree[i][1], weigths[i]
        wtree.append((u, v, w))

    return wtree;


# Undirected, no multiedges and no self-loops
def Graph(N, E):
    edges = {}

    if N == 1: return []

    for _ in range(E):
        u = randrange(1, N + 1)
        v = u
        while v == u: v = randrange(1, N + 1)

        while (u, v) in edges or (v, u) in edges:
            u = randrange(1, N + 1)
            v = u
            while v == u: v = randrange(1, N + 1)

        edges[(u, v)] = 1

    ret = []
    for edge in edges: ret.append(edge)

    return ret;


# Undirected, no multiedges, no self-loops, connected
def ConnectedGraph(N, E):
    E -= N - 1
    tree = Tree(N)
    edges = {}
    for edge in tree:
        edges[edge] = 1

    for _ in range(E):
        u = randrange(1, N + 1)
        v = u
        while v == u: v = randrange(1, N + 1)

        while (u, v) in edges or (v, u) in edges:
            u = randrange(1, N + 1)
            v = u
            while v == u: v = randrange(1, N + 1)

        edges[(u, v)] = 1

    ret = []
    for edge in edges: ret.append(edge)
    
    return ret;


# Undirected, no multiedges, no self-loops, can be forced to be connected
def WGraph(N, E, L, R, connected=False):
    graph = []
    if not connected:
        graph = Graph(N, E)
    else:
        graph = ConnectedGraph(N, E)

    weights = Array(E, L, R)

    wgraph = []
    for i in range(E):
        u, v, w = graph[i][0], graph[i][1], weights[i]
        wgraph.append((u, v, w))
    return wgraph;

