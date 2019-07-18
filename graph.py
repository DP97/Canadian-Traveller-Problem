import random
import math
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay


class graphGen:
    def __init__(self):
        self.G = None
        self.count = 0

    def create(self, n):

        # tvorba uzlov a ich random pozicii
        nodes = []

        for i in range(n):
            nodes.append(i)

        points = []
        points.append((0, 22))

        for j in range(1, len(nodes) - 1):
            x = random.randint(3, 40)
            y = random.randint(3, 40)

            while ((x, y)) in points:
                x = random.randint(3, 40)
                y = random.randint(3, 40)

            points.append((x, y))

        points.append((43, 22))

        t = Delaunay(points)
        edges = []

        # prerobenie uzlov do hran
        m = dict(enumerate(nodes))

        for i in range(t.nsimplex):
            edges.append((m[t.vertices[i, 0]], m[t.vertices[i, 1]]))
            edges.append((m[t.vertices[i, 1]], m[t.vertices[i, 2]]))
            edges.append((m[t.vertices[i, 2]], m[t.vertices[i, 0]]))

        # tvorba grafu
        G = nx.Graph()
        for i in range(len(edges)):
            G.add_edge(edges[i][0], edges[i][1], color="black")

        # pre kazdy uzol vytvorime jeho poziciu (coords) a ulozime ich do grafu
        pos = dict(zip(nodes, points))
        nx.set_node_attributes(G, pos, "pos")

        # pomocne premenne
        ed1 = []
        ed2 = []
        c1 = []
        c2 = []
        coor = 0
        for i in range(len(edges)):
            ed1.append(edges[i][0])
            ed2.append(edges[i][1])

        for i in range(len(edges)):
            c1 = pos[ed1[i]]
            c2 = pos[ed2[i]]

            G[ed1[i]][ed2[i]]["weight"] = math.sqrt(
                ((c2[0] - c1[0]) ** 2) + ((c2[1] - c1[1]) ** 2)
            )
            G[ed1[i]][ed2[i]]["penalty"] = random.randint(5, 10)
            G[ed1[i]][ed2[i]]["propability"] = random.uniform(0, 0.6)

        edges = G.edges()

        colors = []
        for i in range(len(edges)):
            colors.append("black")

        self.graph = G
        return G

    def generate_blockades(self, block_percent):

        # block_percent - percento blokovanych hran

        G = self.graph.copy()
        # odblokovanie vsetkych hran v grafe
        nx.set_edge_attributes(G, "black", "color")

        # pocet hran ktore sa zablokuju podla zadanych %
        count = round(len(G.edges()) / 100 * block_percent)

        # zoznam hran ktore budu blokovane
        blocked = random.sample(list(G.edges()), count)

        # zablokuju sa hrany
        for e in blocked:
            G[e[0]][e[1]]["color"] = "red"

        return G

    def save_fig(self, G):

        pos = nx.get_node_attributes(G, "pos")
        ecolor = [G[e[0]][e[1]]["color"] for e in G.edges()]

        fig = plt.figure(figsize=(10, 10))

        nx.draw_networkx_edges(G, pos, edge_color=ecolor)
        nx.draw_networkx_nodes(G, pos, node_color="r", node_size=80, alpha=1)
        nx.draw(G, pos, edge_color=ecolor, with_labels=True, font_size=7)

        plt.tight_layout(pad=0)
        plt.axis("off")

        plt.savefig("temp/" + "{0:03}".format(self.count) + ".png")
        self.count += 1
