import sys
import heapq
import networkx as nx


class dijkstra:
    def __init__(self, G):
        # vytvorime deep copy grafu
        self.graph = G.copy()
        self.pos = nx.get_node_attributes(G, "pos")
        self.name = "dijkstra"

    def get_path(self, source, target):
        path = []
        path.append(target)

        while target != source:
            target = self.graph.node[target]["previous"]
            path.append(target)

        path.reverse()

        return path

    def get_path_length(self, path):
        # funkcia ktora vrati dlzku trasy
        try:

            sz = len(path)
            cost = 0

            for i in range(0, sz - 2):
                cost += self.graph.get_edge_data(path[i], path[i + 1])["weight"]

            cost += self.graph.get_edge_data(path[sz - 2], path[sz - 1])["weight"]

        except TypeError:
            pass

        return cost

    def shortest_path(self, source, target):
        # nastavenie defaultnych atributov pre vsetky uzly v grafe
        nx.set_node_attributes(self.graph, None, "previous")
        nx.set_node_attributes(self.graph, sys.maxsize, "dist")
        nx.set_node_attributes(self.graph, False, "visited")

        visited = []
        queue = []

        # pociatocny uzol = source, cize vzdialenost = 0
        self.graph.node[source]["dist"] = 0

        # vytvorenie zoznamu s priority algoritmom
        heapq.heappush(queue, (0, source))

        while len(queue) != False:
            # z priority zasobniku vyberieme aktualny uzol
            current = heapq.heappop(queue)
            self.graph.node[current[1]]["visited"] = True

            visited.append(current[1])

            for neighbor in self.graph.neighbors(current[1]):

                if self.graph.node[neighbor]["visited"] == False:
                    distfromstart = (
                        self.graph.node[current[1]]["dist"]
                        + self.graph.get_edge_data(current[1], neighbor)["weight"]
                    )

                if distfromstart < self.graph.node[neighbor]["dist"]:
                    self.graph.node[neighbor]["dist"] = distfromstart
                    self.graph.node[neighbor]["previous"] = current[1]
                    heapq.heappush(queue, (distfromstart, neighbor))

        return self.get_path(source, target)

