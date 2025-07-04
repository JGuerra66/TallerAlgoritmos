import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from time import time
from grafo.crear_grafo import crear_grafo

csv_estudiantes = "data/materias_estudiantes.csv"
csv_profesores = "data/materias_profesores.csv"
output_dir = "resultados"
os.makedirs(output_dir, exist_ok=True)

# --- Definición de Franjas Horarias ---
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORARIOS = ["14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00"]
FRANJAS_HORARIAS = [f"{dia} {hora}" for dia in DIAS for hora in HORARIOS]
MAX_FRANJAS = len(FRANJAS_HORARIAS)

# --- Aplicación de heurísticas ---
def aplicar_heuristica(nombre, strategy, grafo):
    t0 = time()
    colores = nx.coloring.greedy_color(grafo, strategy=strategy)
    t1 = time()
    return {
        "nombre": nombre,
        "colores": colores,
        "cant_colores": max(colores.values()) + 1,
        "tiempo": round(t1 - t0, 4)
    }

# --- Guardar imagen de grafo ---
def guardar_imagen(grafo, colores, titulo, path_salida):
    color_map = [plt.cm.tab20(colores[n] % 20) for n in grafo.nodes()]
    plt.figure(figsize=(14, 10))
    nx.draw(grafo, with_labels=True, node_color=color_map, node_size=1000, font_size=8)
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(path_salida)
    plt.close()

# --- Generar Horario en CSV ---
def generar_horario_csv(nombre_heuristica, colores, franjas, path_salida):
    """Genera un archivo CSV con el horario de exámenes."""
    with open(path_salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Materia", "Día", "Horario"])
        
        mapeo_franjas = {i: franjas[i] for i in range(len(franjas))}

        for materia, color in sorted(colores.items()):
            if color < len(mapeo_franjas):
                franja_completa = mapeo_franjas[color]
                dia, hora = franja_completa.split(" ", 1)
                writer.writerow([materia, dia, hora])

# --- Generar informe ---
def generar_md(resultados, path_salida):
    with open(path_salida, "w", encoding="utf-8") as f:
        f.write("# Comparación de Heurísticas para Asignación de Horarios\n\n")
        f.write(f"Se dispone de **{MAX_FRANJAS}** franjas horarias (Lunes a Viernes, de 14:00 a 22:00).\n\n")
        f.write("## Resultados de las Heurísticas\n\n")
        f.write("| Heurística      | Colores Usados | ¿Solución Válida? | Tiempo (s) |\n")
        f.write("|-----------------|----------------|-------------------|------------|\n")
        for r in resultados:
            f.write(f"| {r['nombre']:<15} | {r['cant_colores']:^14} | {r['solucion_valida']:^17} | {r['tiempo']:^10} |\n")
        
        f.write("\n## Observaciones\n\n")
        f.write("Una solución es **válida** si el número de colores (franjas horarias) que necesita es menor o igual al total de franjas disponibles.\n\n")
        
        soluciones_validas = [r for r in resultados if r['solucion_valida'] == "Sí"]
        if not soluciones_validas:
            f.write("**No se encontró ninguna solución válida con las heurísticas probadas.**\n")
        else:
            mejor_heuristica = min(soluciones_validas, key=lambda x: x['cant_colores'])
            f.write(f"La heurística más eficiente fue **{mejor_heuristica['nombre']}**, que encontró una solución con **{mejor_heuristica['cant_colores']}** colores.\n")
            f.write(f"El horario detallado generado por esta heurística se puede encontrar en `resultados/horario_{mejor_heuristica['nombre'].lower().replace(' ', '_')}.csv`.\n")

# --- MAIN ---
if __name__ == "__main__":
    print("Construyendo grafo...")
    grafo = crear_grafo(csv_estudiantes, csv_profesores)

    print("Aplicando heurísticas...\n")
    heuristicas = [
        ("Greedy", "random_sequential"),
        ("Welsh-Powell", "largest_first"),
        ("DSATUR", "saturation_largest_first")
    ]

    resultados = []
    for nombre, strategy in heuristicas:
        res = aplicar_heuristica(nombre, strategy, grafo)
        
        if res['cant_colores'] <= MAX_FRANJAS:
            res['solucion_valida'] = "Sí"
            path_csv = os.path.join(output_dir, f"horario_{nombre.lower().replace(' ', '_')}.csv")
            generar_horario_csv(nombre, res['colores'], FRANJAS_HORARIAS, path_csv)
            print(f"-> {nombre}: {res['cant_colores']} colores. ✅ Solución válida generada en '{path_csv}'")
        else:
            res['solucion_valida'] = "No"
            print(f"-> {nombre}: {res['cant_colores']} colores. ❌ No es una solución válida (se necesitan más de {MAX_FRANJAS} franjas).")

        resultados.append(res)
        path_img = os.path.join(output_dir, f"{nombre.lower().replace(' ', '_')}_grafo.png")
        guardar_imagen(grafo, res["colores"], f"Grafo coloreado - {nombre}", path_img)

    generar_md(resultados, os.path.join(output_dir, "comparacion.md"))
    print("\n✅ Proceso completado. Resultados guardados en la carpeta 'resultados/'")

