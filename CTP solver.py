import sys
import math
import os
import random

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QFileDialog
from PyQt5.QtGui import QPen, QImage, QPixmap, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt, QLocale

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from graph import graphGen
from dijkstra import dijkstra
from greedy import greedyStrategy
from reposition import repositionStrategy
from comparison import comparisonStrategy
from waiting import waitingStrategy
from recoverygreedy import recoverygreedyStrategy

GREEDY = 0
REPOSITION = 1
COMPARISON = 2
WAITING = 3
RECOVERY_GREEDY = 4
DIJKSTRA = 5


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("gui.ui", self)
        self.setWindowTitle("CTP solver")

        self.figure = plt.figure(figsize=(20, 15))
        # self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

        # pridame sloty
        self.pbExit.clicked.connect(self.close)
        self.pbRun.clicked.connect(self.run)
        self.pbGenerate.clicked.connect(self.generate)

        # vykresleni test grafu
        # self.plot()

        # testovani vykresleni NX grafu
        self.graphGen = graphGen()

        # original_graph = self.graphGen.create(10)
        # self.plot_nx(original_graph)

    def plot_nx(self, graph):
        self.figure.clf()

        G = graph
        pos = nx.get_node_attributes(G, "pos")
        ecolor = [G[e[0]][e[1]]["color"] for e in G.edges()]

        nx.draw_networkx_edges(G, pos, edge_color=ecolor)
        nx.draw_networkx_nodes(G, pos, node_color="r", node_size=80, alpha=1)
        nx.draw(G, pos, edge_color=ecolor, with_labels=True, font_size=7)

        plt.tight_layout()
        self.canvas.draw_idle()
        # self.canvas.draw()

    # vykresleni testovaciho grafu
    def plot(self):
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(data, "*-")

        # refresh canvas
        self.canvas.draw()

    def generate(self):

        nodes = self.sbNodes.value()
        block_pct = self.sbBlockPercent.value()
        self.plainTextEdit.clear()

        self.original_graph = self.graphGen.create(nodes)
        self.original_graph = self.graphGen.generate_blockades(block_pct)
        self.plot_nx(self.original_graph)

    def run(self):

        G = self.original_graph.copy()
        nodes = self.sbNodes.value()

        try:

            controll = False
            path = []
            path_len = 0
            method = self.cbAlgos.currentIndex()

            if method == GREEDY:

                greedy = greedyStrategy(G)
                elapsed, cost, path = greedy.search(0, nodes - 1)

            elif method == REPOSITION:

                reposition = repositionStrategy(G)
                elapsed, cost, path = reposition.search(0, nodes - 1)

            elif method == COMPARISON:

                comparison = comparisonStrategy(G)
                elapsed, cost, path = comparison.search(0, nodes - 1)

            elif method == WAITING:

                waiting = waitingStrategy(G)
                elapsed, cost, path = waiting.search(0, nodes - 1)

            elif method == RECOVERY_GREEDY:

                recoverygreedy = recoverygreedyStrategy(G)
                elapsed, cost, path = recoverygreedy.search(0, nodes - 1)

            elif method == DIJKSTRA:
                djk = dijkstra(G)
                path = djk.shortest_path(0, nodes - 1)
                cost = djk.get_path_length(path)

            else:
                return

            self.printPathInfo(cost, path)
            if method != REPOSITION:
                self.show_path(G, path)
            self.plot_nx(G)

        except KeyError:
            QMessageBox.about(self, "Error!", "Priechodná cesta neexistuje!")
            return

    def show_path(self, G, path):
        # zvyraznime cestu
        for i in range(len(path) - 1):
            G[path[i]][path[i + 1]]["color"] = "dodgerblue"

    def printPathInfo(self, path_len, path):

        # self.plainTextEdit.setPlainText("Path length: " + str(path_len))
        self.plainTextEdit.setPlainText("Path length: " + "{:.2f}".format(path_len))

        s = str()
        for i in range(0, len(path) - 2):
            s += str(path[i]) + "->"

        s += str(path[len(path) - 1])
        self.plainTextEdit.appendPlainText("Shortest path: " + s)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
