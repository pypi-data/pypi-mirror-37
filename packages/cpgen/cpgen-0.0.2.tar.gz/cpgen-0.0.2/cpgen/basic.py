from random import *


# Generate a random array of **INTEGERS** with elements in the range [A, B]
def array(n, a, b):
    arr = [randrange(a, b + 1) for _ in range(n)]
    return arr


# Generate random array of **REAL** with elements in the range [a, b]
def arrayreal(n, a, b):
    arr = [uniform(a, b + 1) for _ in range(n)]
    return arr


# Generate random matrix of size N*N with random integers
'''
# print matrix with space b/w numbers in range [A,B]
for row in matrix:
    print(' '.join(map(str, row)))
'''


# random elements
def matrix(n, a, b):
    m = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            m[r][c] = randint(a, b)
    return m


# with zero at diagonal element
def zdmatrix(n, a, b):
    m = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            m[r][c] = randint(a, b) if r != c else 0
    return m


# symmetric matrix
def symmatrix(n, a, b):
    m = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(r + 1):
            m[r][c] = m[c][r] = randint(a, b)
    return m


# Generate a random string from characters in the range [a, b]
def string(n, a, b):
    l = array(n, ord(a), ord(b))
    s = ''
    for char in l:
        s += chr(char)
    return s


# Generate a random permutation of [1, 2 ... N]
def permutation(n):
    p = list(range(1, n + 1))
    shuffle(p)
    return p
