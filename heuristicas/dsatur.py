# heuristicas/dsatur.py
import networkx as nx

def aplicar_dsatur(grafo):
    return nx.coloring.greedy_color(grafo, strategy='saturation_largest_first')
