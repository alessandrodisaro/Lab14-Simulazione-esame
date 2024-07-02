import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.bestPathAttuale = []

    def creaGrafo(self):
        nodi = DAO.getNodi()
        self.grafo.add_nodes_from(nodi)

        for c1 in nodi:
            for c2 in nodi:
                if c1 != c2:
                    correlation = DAO.getCorrelazione(c1, c2)
                    if correlation is not None:
                        self.grafo.add_edge(c1, c2, weight=correlation)

        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def getPesi(self):
        min = 100000000
        max = -100000000
        for arco in self.grafo.edges.data():
            if arco[1] != arco[0]:
                if arco[2]["weight"] < min:
                    min = arco[2]["weight"]
                if arco[2]["weight"] > max:
                    max = arco[2]["weight"]
        return min, max

    def getSoglie(self, soglia):
        minori = 0
        maggiori = 0
        for arco in self.grafo.edges.data():
            if arco[2]["weight"] > soglia:
                maggiori += 1
            elif arco[2]["weight"] < soglia:
                minori += 1
        return minori, maggiori

    def inizializzazione(self, soglia):
        self.ricorsione(soglia, list(self.grafo.nodes)[0])
        return self.bestPathAttuale

    def ricorsione(self, soglia, parziale):
        # condizione terminale
        if self.grafo.degree(parziale[-1]) == 0:
            maxAttuale = self.calcolaSomma(parziale)
            if maxAttuale > self.calcolaSomma(self.bestPathAttuale):
                self.bestPathAttuale = copy.deepcopy(parziale)
                return
        else:
            nextPossibili = self.grafo.neighbors(parziale[-1])
            # filtro quelli maggiori della soglia
            nextLegali = []
            for nodo in nextPossibili:
                if nodo["weight"] > soglia:
                    nextLegali.append(nodo)
            if len(nextLegali) > 0:
                for next in nextLegali:
                    parziale.append(next)
                self.ricorsione(soglia, parziale)
            parziale.pop()

    def calcolaSomma(self, parziale):
        pesoTot = 0

        for tappa in parziale:
            pesoTot += tappa["weight"]

        return pesoTot
