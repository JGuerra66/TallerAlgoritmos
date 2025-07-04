# heuristicas/welsh_powell.py
import networkx as nx

def aplicar_welsh_powell(grafo):
    return nx.coloring.greedy_color(grafo, strategy='largest_first')
