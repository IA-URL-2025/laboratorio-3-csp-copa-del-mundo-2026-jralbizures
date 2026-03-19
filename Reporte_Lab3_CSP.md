# Laboratorio 3: El sorteo de la Copa del Mundo 2026 como CSP

**Nombre:** Jackeline Raquel Albizures Quevedo
**Carné:** 1122323
**Fecha:** 18/03/2026

---

## Introducción

El sorteo de la Copa del Mundo 2026 constituye un problema complejo que puede ser analizado desde la perspectiva de la **Inteligencia Artificial (IA)**, específicamente como un **Problema de Satisfacción de Restricciones (CSP, Constraint Satisfaction Problem)**. Este enfoque permite representar formalmente la asignación de selecciones nacionales a grupos bajo un conjunto de reglas estrictas establecidas por la FIFA.

En este contexto, el problema consiste en asignar equipos a los grupos A–L respetando restricciones relacionadas con confederaciones, bombos, equipos anfitriones y playoffs intercontinentales. Este tipo de problema es ideal para aplicar técnicas como **backtracking**, junto con heurísticas como **MRV (Minimum Remaining Values)** y **Forward Checking**, que permiten reducir el espacio de búsqueda y encontrar soluciones válidas de manera eficiente.

El caso central de este análisis es el **Grupo K**, conformado por **Portugal, Irán, Uzbekistán y el Playoff Inter-2**, el cual presenta una aparente inconsistencia al incluir dos equipos de la confederación AFC. Este caso será utilizado como hilo conductor para explicar cómo los modelos CSP manejan restricciones complejas y situaciones ambiguas.

---

# Sección 1 — Modelado del problema como CSP

## Variables

El Mundial 2026 está compuesto por:

- **12 grupos (A–L)**
- **4 posiciones por grupo (Bombo 1, 2, 3 y 4)**

Dado que los equipos de los **Bombos 1 y 2 ya están asignados**, las variables del CSP corresponden a:

- Las **12 posiciones del Bombo 3**
- Las **12 posiciones del Bombo 4**

En total, el problema involucra **24 variables**.

---

## Dominios

El dominio de cada variable está formado por los equipos disponibles en cada bombo:

- **Bombo 3:** selecciones intermedias
- **Bombo 4:** selecciones restantes + placeholders de playoffs

Los placeholders (ej. _Playoff Inter-2_) representan posibles equipos de diferentes confederaciones, lo que introduce incertidumbre en el modelo.

---

## Restricciones

### 1. Confederaciones

- Máximo **1 equipo por confederación por grupo**
- Excepción: **UEFA puede tener hasta 2 equipos**

### 2. Bombos

- Cada grupo debe tener exactamente un equipo de cada bombo

### 3. Equipos anfitriones

- México → Grupo A
- Canadá → Grupo B
- Estados Unidos → Grupo D

### 4. Playoffs intercontinentales

- Representan múltiples confederaciones
- No pertenecen a una sola confederación fija

### 5. Balance UEFA

- Algunos grupos deben contener exactamente 2 equipos UEFA

---

## Tabla de grupos (representación)

| Grupo | Bombo 1        | Bombo 2 | Bombo 3    | Bombo 4         |
| ----- | -------------- | ------- | ---------- | --------------- |
| A     | México         | Equipo  | Equipo     | Equipo          |
| B     | Canadá         | Equipo  | Equipo     | Equipo          |
| C     | Equipo         | Equipo  | Equipo     | Equipo          |
| D     | Estados Unidos | Equipo  | Equipo     | Equipo          |
| E     | Equipo         | Equipo  | Equipo     | Equipo          |
| F     | Equipo         | Equipo  | Equipo     | Equipo          |
| G     | Equipo         | Equipo  | Equipo     | Equipo          |
| H     | Equipo         | Equipo  | Equipo     | Equipo          |
| I     | Francia        | Noruega | Equipo     | Playoff Inter-1 |
| J     | Equipo         | Equipo  | Equipo     | Equipo          |
| K     | Portugal       | Irán    | Uzbekistán | Playoff Inter-2 |
| L     | Equipo         | Equipo  | Equipo     | Equipo          |

---

## Grupos con tensiones aparentes

- **Grupo K:** dos equipos AFC (Irán y Uzbekistán)
- **Grupo D:** influencia de anfitriones
- **Grupo I:** interacción con Playoff Inter-1

---

# Sección 2 — El conflicto

El **Grupo K** presenta una aparente violación de las reglas:

- Portugal (UEFA)
- Irán (AFC)
- Uzbekistán (AFC)
- Playoff Inter-2

Según la regla general, no deberían existir dos equipos AFC en el mismo grupo.

---

## Explicación del conflicto

El **Playoff Inter-2** está compuesto por:

- Bolivia (CONMEBOL)
- Surinam (CONCACAF)
- Irak (AFC)

Esto implica que el playoff no pertenece a una única confederación, sino que es un **conjunto multi-confederación**.

---

## Interpretación correcta

- El placeholder no representa un equipo fijo
- Se consideran múltiples posibles resultados
- No se garantiza un tercer equipo AFC

---

## Diferencia clave

- **Violación aparente:** dos equipos AFC visibles
- **Realidad:** el tercer slot es incierto

---

## Conclusión del conflicto

El modelo CSP resuelve este problema al considerar:

- Dominios variables
- Restricciones dinámicas
- Incertidumbre en los playoffs

---

# Sección 3 — La causa (análisis técnico IA)

## Heurísticas

### MRV (Minimum Remaining Values)

Selecciona la variable con menos opciones posibles.

Ejemplo:

- Grupo K tiene menos opciones → se evalúa primero

---

### LCV (Least Constraining Value)

Selecciona el valor que menos restringe a otras variables.

---

### Forward Checking

Después de cada asignación:

- Reduce dominios de otras variables
- Detecta conflictos temprano

---

## Pseudotraza

```

1. Seleccionar variable: Grupo K - Bombo 3
2. Intentar: Uzbekistán
3. Validación: válida
4. Aplicar Forward Checking
5. Reducir dominios
6. Seleccionar siguiente variable (MRV)
7. Intentar asignación en Grupo I
8. Dominio vacío detectado
9. Backtracking
10. Probar nuevo valor
11. Validación correcta
12. Continuar

```

---

## Relación con Grupo I

El Grupo I presenta un caso similar debido al:

- Playoff Inter-1
- Restricciones UEFA

Esto permite comparar cómo los playoffs afectan el modelo CSP.

---

# Sección 4 — La solución IA

## Enfoque

Se utiliza:

- **Backtracking**
- **Forward Checking**
- Heurísticas MRV y LCV

---

## Pseudocódigo

```pseudo
function BACKTRACK(assignment, domains):
    if assignment completo:
        return assignment

    var = seleccionar_variable_MRV(domains)

    for valor in ordenar_por_LCV(var):
        if es_valido(var, valor, assignment):
            assignment[var] = valor

            nuevos_dominios = forward_check(var, valor, domains)

            if nuevos_dominios != fallo:
                resultado = BACKTRACK(assignment, nuevos_dominios)
                if resultado != fallo:
                    return resultado

            eliminar assignment[var]

    return fallo
```

---

## Validación

```pseudo
function es_valido(var, valor, assignment):
    verificar_confederaciones()
    verificar_bombo()
    verificar_UEFA()
    verificar_playoffs()
    return true/false
```

---

## Complejidad

- Peor caso: **O(b^n)**
- b = tamaño del dominio
- n = número de variables

---

## Optimización

Las heurísticas permiten:

- Reducir el espacio de búsqueda
- Detectar errores temprano
- Evitar combinaciones inválidas

---

# Conclusiones

El modelado del sorteo como un **CSP** permite resolver un problema real con múltiples restricciones.

El caso del **Grupo K** demuestra que:

- No todas las inconsistencias son errores
- La interpretación correcta del modelo es clave
- Los playoffs requieren tratamiento especial

Las técnicas de IA utilizadas permiten encontrar soluciones válidas de forma eficiente, evidenciando la utilidad del enfoque CSP en problemas del mundo real.

---

# Referencias

- Russell, S. & Norvig, P. (2020). _Artificial Intelligence: A Modern Approach_ (4.ª ed.), Capítulo 6.
- FIFA (2025). Procedimientos del sorteo final del Mundial 2026.
