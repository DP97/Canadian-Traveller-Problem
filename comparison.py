from dijkstra import *
from timeit import default_timer as timer
import random

import matplotlib.pyplot as plt
import networkx as nx


class comparisonStrategy(dijkstra):
    def __init__(self, G):
        dijkstra.__init__(self, G)
        self.name = "Comparison strategy"

    def search(self, source, target):
        G = self.graph.copy()

        start = timer()

        path = self.shortest_path(source, target)

        route = []
        route.append(path[0])

        total_cost = 0
        costGS = 0
        costRS = 0
        costRUN = 0

        i = 0

        while route[-1] != target:
            if self.graph.get_edge_data(path[i], path[i + 1])["color"] != "red":
                route.append(path[i + 1])
                total_cost += self.graph.get_edge_data(path[i], path[i + 1])["weight"]
                costRUN += self.graph.get_edge_data(path[i], path[i + 1])["weight"]
                i += 1
            else:
                self.graph.remove_edge(path[i], path[i + 1])
                costGS = self.get_path_length(self.shortest_path(path[i], target))
                costRS = self.get_path_length(self.shortest_path(source, target))

                if costGS <= (costRS + costRUN):
                    path = self.shortest_path(path[i], target)
                else:
                    total_cost += costRUN
                    costRUN = 0
                    path = self.shortest_path(source, target)
                i = 0

        end = timer()
        elapsed = end - start

        print("Search time:", elapsed)
        print("Path: ", route)
        print("Path length:", total_cost)

        self.graph = G

        return elapsed, total_cost, route
