# heuristicas/greedy.py
import networkx as nx

def aplicar_greedy(grafo):
    return nx.coloring.greedy_color(grafo, strategy='random_sequential')
