import csv
import networkx as nx
from collections import defaultdict

def crear_grafo(estudiantes_csv, profesores_csv):
    # Materias y estudiantes
    materias_estudiantes = defaultdict(set)

    with open(estudiantes_csv, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            estudiante = row["estudiante"]
            materia = row["materia"]
            materias_estudiantes[materia].add(estudiante)

    # Materias y profesores
    materias_profesor = defaultdict(set)

    with open(profesores_csv, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            materia = row["materia"]
            profesor = row["profesor"]
            materias_profesor[profesor].add(materia)

    # Crear grafo
    materias = list(materias_estudiantes.keys())
    G = nx.Graph()
    G.add_nodes_from(materias)

    # Aristas por estudiantes en común
    for i in range(len(materias)):
        for j in range(i + 1, len(materias)):
            m1, m2 = materias[i], materias[j]
            if materias_estudiantes[m1] & materias_estudiantes[m2]:
                G.add_edge(m1, m2)

    # Aristas por profesores en común
    for materias_del_profesor in materias_profesor.values():
        materias_lista = list(materias_del_profesor)
        for i in range(len(materias_lista)):
            for j in range(i + 1, len(materias_lista)):
                G.add_edge(materias_lista[i], materias_lista[j])

    return G
