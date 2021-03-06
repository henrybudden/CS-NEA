graph = {'A1': ['B1', 'A2'],
         'A2': ['B2', 'A1', 'A3'],
         'A3': ['B3', 'A2', 'A4'],
         'A4': ['B4', 'A3', 'A5'],
         'A5': ['B5', 'A4'],
         'B1': ['A1', 'B2', 'C1'],
         'B2': ['A2', 'B1', 'B3'],
         'B3': ['A3', 'B2', 'B4'],
         'B4': ['A4', 'B3', 'B5'],
         'B5': ['A5', 'B4','C5'],
         'C1': ['B1', 'D1'],
         'C5': ['B5', 'D5'],
         'E1': ['D1', 'E2', 'F1'],
         'D1': ['E1', 'D2', 'C1'],
         'D2': ['E2', 'D1', 'D3'],
         'D3': ['E3', 'D2', 'D4'],
         'D4': ['E4', 'E3', 'E5'],
         'D5': ['E5', 'D4', 'C5'],
         'E2': ['D2', 'E1', 'E3'],
         'E3': ['D3', 'E2', 'E4'],
         'E4': ['D4', 'E3', 'E5'],
         'E5': ['D5', 'E4', 'F5'],
         'F1': ['E1', 'G1'],
         'F5': ['E5', 'G5'],
         'G1': ['H1', 'G2', 'F1'],
         'G2': ['H2', 'G1', 'G3'],
         'G3': ['H3', 'G2', 'G4'],
         'G4': ['H4', 'H3', 'H5'],
         'G5': ['H5', 'G4', 'F5'],
         'H1': ['G1', 'H2', 'I1'],
         'H2': ['G2', 'H1', 'H3'],
         'H3': ['G3', 'H2', 'H4'],
         'H4': ['G4', 'H3', 'H5'],
         'H5': ['G5', 'H4', 'I5'],
         'I1': ['H1', 'J1'],
         'I5': ['H5', 'J5'],
         'J1': ['K1', 'J2', 'I1'],
         'J2': ['K2', 'J1', 'J3'],
         'J3': ['K3', 'J2', 'J4'],
         'J4': ['K4', 'J3', 'J5'],
         'J5': ['K5', 'G4', 'I5'],
         'K1': ['J1', 'K2'],
         'K2': ['J2', 'K1', 'K3'],
         'K3': ['J3', 'K2', 'K4'],
         'K4': ['J4', 'K3', 'K5'],
         'K5': ['J5', 'K4']
         }
         

def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

start_location = input("Enter start location: ")
end_location = input("Enter end location: ")
print("shortest path", find_shortest_path(graph, start_location, end_location))

