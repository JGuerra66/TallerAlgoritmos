# Taller 1 - Asignación de horarios sin superposición

Este proyecto aborda el problema de asignar franjas horarias a exámenes finales de una institución educativa, evitando superposición entre materias que comparten estudiantes o docentes.

## 🎯 Objetivo

Asignar el **mínimo número de franjas horarias** a materias de forma tal que:
- Materias que comparten al menos un estudiante no se superpongan.
- Materias que tienen el mismo docente tampoco se solapen.

## 📊 Modelo

El problema se modela como un **grafo de conflictos**, donde:

- **Nodos**: materias
- **Aristas**: existe una si dos materias comparten al menos un estudiante o un profesor
- **Colores**: franjas horarias asignadas (máximo 20 posibles)


## 🧠 Heurísticas aplicadas

Se aplican tres estrategias para resolver el coloreo del grafo:

- 🎨 **Greedy** (`random_sequential`)
- 🧱 **Welsh-Powell** (`largest_first`)
- 🔍 **DSATUR** (`saturation_largest_first`)

## 🧪 Ejecución

### 1. Instalar dependencias

```bash
pip install networkx matplotlib
```

### 2. Ejecutar el script principal

```bash
python main.py
```

Los resultados se guardarán en la carpeta `resultados/`.

## 📌 Consideraciones

- Se define un conjunto de **20 franjas horarias posibles** (Lunes a Viernes, de 14:00 a 22:00).
- Se considera que una solución es válida si no usa más de 20 colores.
- En caso de haber múltiples soluciones válidas, se destaca la más eficiente (menor cantidad de colores).

