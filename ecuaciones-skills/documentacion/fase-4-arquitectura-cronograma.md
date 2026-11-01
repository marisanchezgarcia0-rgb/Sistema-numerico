# Fase 4 — Arquitectura, estructura del proyecto y cronograma

## 4.1 Arquitectura

```
Usuario
  |  "Usa la skill y resuelve: 2x + y = 5, x - y = 1"
  v
IA (Claude)
  |  1. Lee la descripción de las skills y elige una
  |  2. Lee el SKILL.md completo
  |  3. Convierte las ecuaciones a JSON {A, b}
  v
Script de Python  (scripts/resolver_lineal.py)
  |  Cálculo exacto + pasos  ->  JSON de salida
  v
IA (Claude)
  |  Lee el JSON y redacta la respuesta con el formato fijo
  v
Usuario: sistema interpretado, procedimiento, resultado, verificación
```

**Reparto de responsabilidades**

| Quién | Hace | No hace |
|-------|------|---------|
| IA | Entender el enunciado, armar `A` y `b`, ejecutar el script, explicar | Calcular a mano |
| Script | Calcular, clasificar el sistema, listar los pasos | Interpretar lenguaje natural |
| `SKILL.md` | Decir a la IA qué hacer y en qué formato | Contener cálculos |

## 4.2 Principios de diseño

- **La IA lee y explica; el script calcula.**
- **Una skill, una carpeta:** agregar una skill no obliga a tocar las demás.
- **Entrada y salida en JSON:** formato claro para la IA y fácil de probar.
- **Errores controlados:** un dato inválido produce un mensaje, nunca un error sin explicar.
- **Los scripts funcionan solos:** se pueden usar y probar sin ninguna IA.

## 4.3 Estructura del proyecto

El proyecto se separa en dos carpetas: **`documentacion/`** (todo lo escrito) y **`sistema/`** (todo lo que hace funcionar el programa).

```
ecuaciones-skills/
├── README.md
├── documentacion/
│   ├── Planificacion_..._Fases_1-4.docx
│   └── fase-1 ... fase-4 (.md)
└── sistema/
    ├── skills/
    │   ├── resolver-sistema-lineal/
    │   │   ├── SKILL.md
    │   │   └── scripts/resolver_lineal.py
    │   ├── metodos-iterativos/
    │   │   ├── SKILL.md
    │   │   └── scripts/iterativos.py
    │   ├── regla-de-cramer/
    │   │   ├── SKILL.md
    │   │   └── scripts/cramer.py
    │   └── matriz-inversa/
    │       ├── SKILL.md
    │       └── scripts/inversa.py
    ├── tests/test_skills.py
    ├── ejemplos/           (JSON de ejemplo)
    ├── evaluacion/         (batería de 24 sistemas, día 9)
    └── interfaz/           (Streamlit, opcional)
```

## 4.4 Anatomía de un `SKILL.md`

| Parte | Contenido | Por qué importa |
|-------|-----------|-----------------|
| Encabezado (`name`, `description`) | Nombre y descripción de cuándo usarla | La IA decide con esto si la activa |
| Cuándo usar | Situaciones y límites (qué no cubre) | Evita usos incorrectos |
| Regla principal | "No hagas la aritmética tú mismo" | Garantiza exactitud |
| Procedimiento | Pasos numerados: interpretar, preparar JSON, ejecutar, leer | La IA lo sigue igual cada vez |
| Formato de respuesta | Estructura fija | Respuestas consistentes |
| Ejemplo | Una entrada y su resultado esperado | Calibra a la IA |

## 4.5 Contrato de los scripts

**Entrada** (`resolver_lineal.py`):

```json
{"A": [[2, 1], [1, -1]], "b": [5, 1]}
```

**Salida:**

```json
{
  "ok": true,
  "tipo": "unica",
  "solucion": ["x1 = 2", "x2 = 1"],
  "pasos": ["Matriz aumentada [A|b]: ...", "F1 = F1 / (2)", "..."],
  "explicacion": "El sistema tiene solución única: x1 = 2, x2 = 1."
}
```

**Error:** `{"ok": false, "error": "ValueError: ..."}` con código de salida 1.

## 4.6 Cronograma de 2 semanas

Las 4 skills siguen el mismo patrón (script que lee JSON y devuelve JSON, más un `SKILL.md`). Por eso se aprende el patrón a fondo con la primera skill y las siguientes avanzan más rápido. El `SKILL.md` de cada skill se escribe **el mismo día** que su script.

### Semana 1 — Skill 1 y base del proyecto

| Día | Entregable | Aprendizaje clave |
|-----|-----------|-------------------|
| 1 | Entorno listo (Python, VS Code, Git). **Prueba de que la IA usa skills** con una skill de ejemplo. Repositorio creado | Qué es una skill; verificar el acceso |
| 2 | Skill 1 `resolver-sistema-lineal`: lectura del JSON y eliminación de Gauss-Jordan con `Fraction` | Listas de listas, JSON |
| 3 | Clasificación del sistema (única, infinitas, sin solución) y manejo de errores | Casos límite |
| 4 | Pruebas con pytest y `SKILL.md` de la skill 1 | pytest, redactar instrucciones |
| 5 | Prueba de la skill 1 con la IA con 10 sistemas. **Hito 1** | Evaluar y ajustar la descripción |

### Semana 2 — Skills 2 a 4, evaluación y cierre

| Día | Entregable | Aprendizaje clave |
|-----|-----------|-------------------|
| 6 | Skill 2 `metodos-iterativos` (Jacobi y Gauss-Seidel) con tabla de iteraciones, pruebas y `SKILL.md` | Ciclos, convergencia |
| 7 | Skill 3 `regla-de-cramer`: determinante exacto, matrices Ai, pruebas y `SKILL.md` | Determinantes; reutilizar el patrón |
| 8 | Skill 4 `matriz-inversa` (Gauss-Jordan sobre [A \| I]), pruebas y `SKILL.md`; prueba cruzada entre las tres skills exactas | Reutilizar código; contrastar resultados |
| 9 | Batería de 24 sistemas evaluada con la IA; ajuste de las descripciones para que elija bien entre skills parecidas. **Hito 2** | Medir la calidad |
| 10 | README, ensayo y demo, entrega. **Hito 3** | Explicar el proyecto |

> **Nota de realismo:** la semana 2 es ajustada, porque hay 3 skills en 3 días. El repositorio incluye una implementación de referencia de las cuatro skills. El equipo debe construir cada skill y puede comparar con la de referencia al terminar; si alguien se atrasa, trabaja en pareja a partir de ella (ver reglas de contingencia).

### Hitos y criterio de control

| Hito | Día | Condición para pasar |
|------|-----|----------------------|
| H1 | 5 | Skill 1 con pruebas en verde y la IA la usa correctamente en 9 de 10 casos |
| H2 | 9 | **4 skills operativas** con pruebas en verde y batería de 24 casos con ≥ 90 % de aciertos |
| H3 | 10 | Demo lista y cada integrante explica una skill |

### Reglas de contingencia

- Si la cuenta del equipo **no permite skills** (día 1): se usa el plan alterno de pegar el `SKILL.md` en el chat y ejecutar el script localmente. No cambia el trabajo de programación.
- Si al día 5 la skill 1 no está lista: se pasa a trabajo en pareja y se compara con la implementación de referencia para no frenar las demás. **El mínimo de 4 skills no se recorta.**
- Si al día 9 faltan casos de la batería: se evalúa un mínimo de 12 casos, 3 por cada skill, y se anota lo pendiente.
- **No hay día de colchón.** Las funciones opcionales (quinta skill, Streamlit) solo se empiezan si el Hito 2 se cumple antes del día 9, y se eliminan si no.

## 4.7 Evaluación de las skills

Se arma una tabla con 24 sistemas que cubra:

| Tipo de caso | Cantidad | Skill esperada |
|--------------|----------|----------------|
| Solución única 2×2, 3×3 y 4×4 | 6 | `resolver-sistema-lineal` |
| Con fracciones y decimales | 3 | `resolver-sistema-lineal` |
| Pivote cero (requiere intercambiar filas) | 2 | `resolver-sistema-lineal` |
| Infinitas soluciones | 2 | `resolver-sistema-lineal` |
| Sin solución | 2 | `resolver-sistema-lineal` |
| Datos faltantes o mal escritos (la IA debe preguntar) | 2 | — |
| Jacobi / Gauss-Seidel, incluido uno que no converge | 3 | `metodos-iterativos` |
| Regla de Cramer, incluido un caso con det(A) = 0 | 2 | `regla-de-cramer` |
| Matriz inversa, incluida una matriz singular | 2 | `matriz-inversa` |

Para cada caso se registra: si la IA usó la skill correcta, si ejecutó el script, si el resultado coincide y si respetó el formato. La meta es 90 % o más (22 de 24).

## 4.8 Hoja de ruta de expansión (Etapa 2)

| Orden | Mejora | Esfuerzo | Requisito |
|-------|--------|----------|-----------|
| E1 | Skill de verificación de solución (residuos) | 1 día | MVP terminado |
| E2 | Interfaz Streamlit que llama a los scripts | 1–2 días | MVP terminado |
| E3 | Skill de sistemas no lineales (Newton multivariable) | 2–3 días | Aprender SymPy |
| E4 | Más skills (descomposición LU, mínimos cuadrados, rango de una matriz) | 1–2 días c/u | E1 |
| E5 | Aplicación propia con la API de la IA y las skills | 3–5 días | API key |
| E6 | Historial en SQLite | 1–2 días | E5 |
| E7 | Frontend avanzado en React | 5+ días | E5 y alguien que domine JavaScript |
| E8 | Docker y CI | 1–2 días | MVP terminado |

**Qué se reutiliza:** las skills y los scripts no cambian al crecer. La aplicación propia o el frontend solo se agregan como nuevas formas de llamarlos.

## 4.9 Definición de "terminado" por tarea

- El código funciona y se probó con ejemplos conocidos.
- Tiene pruebas automáticas en verde.
- Otra persona del equipo lo revisó y puede explicarlo.
- Está descrito en el README.
