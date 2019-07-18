from dijkstra import *
from timeit import default_timer as timer
import random

import matplotlib.pyplot as plt
import networkx as nx


class greedyStrategy(dijkstra):
    def __init__(self, G):
        dijkstra.__init__(self, G)
        self.name = "Greedy strategy"


    
    def search(self, source, target):
        G = self.graph.copy()

        start = timer()

        path = self.shortest_path(source, target)

        route = []
        route.append(path[0])
        
        i = 0
        
        while route[-1] != target:
            if self.graph.get_edge_data(path[i], path[i + 1])["color"] != "red":
                route.append(path[i + 1])                
                i += 1
            else:
                self.graph.remove_edge(path[i], path[i + 1])
                path = self.shortest_path(path[i], target)
                i = 0

        
        end = timer()
        elapsed = end - start

        print("Search time:", elapsed)
        print("Path: ", route)
        print("Path length:", self.get_path_length(route))

        self.graph = G

        return elapsed, self.get_path_length(route), route
