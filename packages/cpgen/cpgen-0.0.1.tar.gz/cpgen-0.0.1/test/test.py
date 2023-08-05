from cpgen.graph import *
 
### Test from basic.py ###
# for i in Array(10,-10,100):
#     print(i, end=" ")
#     
# for i in ArrayReal(10, -100, 100):
#     print(i, end=" ")
#  
# for i in Matrix(3, 0, 1):
#     for j in i:
#         print(j, end=" ")
#     print("")
#    
# for i in ZDMatrix(3, -10, 100):
#     for j in i:
#         print(j, end=" ")
#     print("")
# 
# print(String(24, 'a', 'z'))
# 
# for i in Permutation(10):
#     print(i, end=" ")

### graph.py ###
    
# for i in Tree(10):
#     for j in i:
#         print(j,end=" ")
#     print("")

# for i in WTree(10,1,100):
#     for j in i:
#         print(j,end=" ")
#     print("")

for i in Graph(10,20):
    for j in i:
        print(j, end=" ")
    print("")
