from random import *

# Generate a random array of **INTEGERS** with elements in the range [A, B]
def Array(N, A, B):
    arr = [randrange(A, B + 1) for _ in range(N)]
    return arr;


# Generate random array of **REAL** with elements in the range [a, b]
def ArrayReal(N, A, B):
    arr = [uniform(A, B + 1) for _ in range(N)]
    return arr;


# Generate random matrix of size N*N with random integers
'''
# print matrix with space b/w numbers in range [A,B]
for row in matrix:
    print(' '.join(map(str, row)))
'''
# random elements
def Matrix(N, A, B):
    m = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            m[r][c] = randint(A, B)
    return m;


# with zero at diagonal element
def ZDMatrix(N, A, B):
    m = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            m[r][c] = randint(A, B) if r != c else 0 
    return m;

# symmetric matrix
def SymMatrix(N, A, B):
    symmatrix = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(r + 1):
            symmatrix[r][c] = symmatrix[c][r] = randint(A, B)
    return symmatrix;


# Generate a random string from characters in the range [a, b]
def String(N, A, B):
    l = Array(N, ord(A), ord(B))
    s = ''
    for char in l: s += chr(char)
    return s;


# Generate a random permutation of [1, 2 ... N]
def Permutation(N):
    permutation = list(range(1, N + 1))
    shuffle(permutation)
    return permutation;
