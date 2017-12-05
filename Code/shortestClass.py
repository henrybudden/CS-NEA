class ShortestPath():
    graph = {'A1': ['B1', 'A2'],
             'A2': ['B2', 'A1', 'A3'],
             'A3': ['B3', 'A2', 'A4'],
             'A4': ['B4', 'A3', 'A5'],
             'A5': ['B5', 'A4'],
             'B1': ['A1', 'B2', 'C1'],
             'B2': ['A2', 'B1', 'B3'],
             'B3': ['A3', 'B2', 'B4'],
             'B4': ['A4', 'B3', 'B5'],
             'B5': ['A5', 'B4', 'C5'],
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
             'H2': ['G2', 'H1', 'H3', 'I1'],
             'H3': ['G3', 'H2', 'H4', 'I1'],
             'H4': ['G4', 'H3', 'H5', 'I2'],
             'H5': ['G5', 'H4', 'I5', 'I2'],
             'I1': ['H1', 'H2', 'H3'],
             'I2': ['H4', 'H5']
             }

    def __init__(self):
        self.route = []
        

    def find_shortest_path(self, start, end, path=None):
        if path is None:
            path = []

        path = path + [start]
        if start == end:
            return path
        if start not in self.graph:
            return None
        shortest = ""
        for node in self.graph[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path.copy())
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def find_route(self, start, nodes, end, path=None):
        self.route = []
        return self.__find_route(start, nodes, end, path)

    def __find_route(self, start, nodes, end, path=None):
        if path is None:
            path = []

        self.route.append(start)
        if len(nodes) == 0:
            for x in self.find_shortest_path(start, end):
                path.append(x)
            self.route.append(end)
            for x in range(len(path)):
                if path[x] in self.route:
                    node = "*" + str(path[x]) + "*"
                    path[x] = str(node)
            return path
        if start not in self.graph:
            return None
        shortest = ""
        for x in nodes:
            newpath = self.find_shortest_path(start, x)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
        for y in shortest[0:len(shortest) - 1]:
            path.append(y)
        nodes.remove(shortest[len(shortest) - 1])
        self.__find_route(shortest[-1], nodes, end, path)
        path_out = path
        path = []
        return self.route, path_out

    def get_distance(self, start, end):
        route = self.find_route(start, [], end)
        return(len(route)-1)
