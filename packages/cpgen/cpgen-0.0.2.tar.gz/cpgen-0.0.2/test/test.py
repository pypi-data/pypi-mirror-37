from cpgen.graph import *

## Test from basic.py ###
for i in array(10, -10, 100):
    print(i, end=" ")
print("")

for i in arrayreal(10, -100, 100):
    print(i, end=" ")
print("")

for i in matrix(3, 0, 1):
    for j in i:
        print(j, end=" ")
    print("")

for i in zdmatrix(3, -10, 100):
    for j in i:
        print(j, end=" ")
    print("")

print(string(24, 'a', 'z'))

for i in permutation(10):
    print(i, end=" ")

## graph.py ###

for i in tree(10):
    for j in i:
        print(j, end=" ")
    print("")

for i in wtree(10, 1, 100):
    for j in i:
        print(j, end=" ")
    print("")

for i in graph(10, 20):
    for j in i:
        print(j, end=" ")
    print("")

