# Comparación de Heurísticas para Asignación de Horarios

Se dispone de **20** franjas horarias (Lunes a Viernes, de 14:00 a 22:00).

## Resultados de las Heurísticas

| Heurística      | Colores Usados | ¿Solución Válida? | Tiempo (s) |
|-----------------|----------------|-------------------|------------|
| Greedy          |       11       |        Sí         |    0.0     |
| Welsh-Powell    |       11       |        Sí         |    0.0     |
| DSATUR          |       11       |        Sí         |   0.001    |

## Observaciones

Una solución es **válida** si el número de colores (franjas horarias) que necesita es menor o igual al total de franjas disponibles.

La heurística más eficiente fue **Greedy**, que encontró una solución con **11** colores.
El horario detallado generado por esta heurística se puede encontrar en `resultados/horario_greedy.csv`.
