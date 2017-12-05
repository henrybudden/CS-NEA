from shortestClass import *

sh = ShortestPath()

path = sh.__find_route("I1", ["B3", "F1", "G1"], "A5")

print("Order:")
for x in path[0]:
    print(x)
print("Route:")
for x in path[1]:
    print(x)


path = sh.__find_route("I1", ["F5", "H1", "G1"], "A5")

print("Order:")
for x in path[0]:
    print(x)
print("Route:")
for x in path[1]:
    print(x)
