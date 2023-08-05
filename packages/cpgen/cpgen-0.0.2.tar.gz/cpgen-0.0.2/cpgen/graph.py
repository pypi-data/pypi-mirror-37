from random import *
from cpgen.basic import *


# Generate a random unweighted tree
def tree(n):
    edges = []
    for u in range(2, n + 1):
        v = randrange(1, u)
        edges.append([u, v])

    permute = permutation(n)

    for i in range(0, n - 1):
        u, v = edges[i]
        u = permute[u - 1]
        v = permute[v - 1]
        edges[i] = (u, v)
    return edges


# Generate a random weighted tree
def wtree(n, l, r):
    weigths = array(n - 1, l, r)
    t = tree(n)
    wtree = []

    for i in range(0, n - 1):
        u, v, w = t[i][0], t[i][1], weigths[i]
        wtree.append((u, v, w))

    return wtree


# Undirected, no multiedges and no self-loops
def graph(n, e):
    edges = {}

    if n == 1:
        return []

    for _ in range(e):
        u = randrange(1, n + 1)
        v = u
        while v == u:
            v = randrange(1, n + 1)

        while (u, v) in edges or (v, u) in edges:
            u = randrange(1, n + 1)
            v = u
            while v == u:
                v = randrange(1, n + 1)

        edges[(u, v)] = 1

    ret = []
    for edge in edges:
        ret.append(edge)

    return ret


# Undirected, no multiedges, no self-loops, connected
def connectedgraph(n, e):
    e -= n - 1
    t = tree(n)
    edges = {}
    for edge in t:
        edges[edge] = 1

    for _ in range(e):
        u = randrange(1, n + 1)
        v = u
        while v == u:
            v = randrange(1, e + 1)

        while (u, v) in edges or (v, u) in edges:
            u = randrange(1, n + 1)
            v = u
            while v == u:
                v = randrange(1, n + 1)

        edges[(u, v)] = 1

    ret = []
    for edge in edges:
        ret.append(edge)

    return ret;


# Undirected, no multiedges, no self-loops, can be forced to be connected
def wgraph(n, e, l, r, connected=False):
    g = []
    if not connected:
        g = graph(n, e)
    else:
        g = connectedgraph(n, e)

    weights = array(e, l, r)

    wgraph = []
    for i in range(e):
        u, v, w = g[i][0], g[i][1], weights[i]
        wgraph.append((u, v, w))
    return wgraph
