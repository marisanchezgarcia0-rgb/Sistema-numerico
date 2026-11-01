# Fase 2 — Análisis de requerimientos

## 2.1 Actores

| Actor | Descripción | Necesidad principal |
|-------|-------------|---------------------|
| Usuario (estudiante) | Entrega un sistema de ecuaciones y quiere la solución | No repetir instrucciones y ver el procedimiento |
| Docente | Revisa o prepara ejercicios | Resultados correctos y reproducibles |
| IA (Claude) | Lee la skill, interpreta el problema y ejecuta el script | Instrucciones claras, sin ambigüedad |
| Desarrollador | Crea y mantiene skills | Una estructura estándar fácil de seguir |

## 2.2 Requerimientos funcionales

**Etapa:** MVP (2 semanas), Opc. (opcional si se cumple el Hito 2) o Exp. (Etapa 2).

| ID | Requerimiento | Prioridad | Etapa |
|----|---------------|-----------|-------|
| RF-01 | Cada skill es una carpeta con `SKILL.md` y `scripts/` | Alta | MVP |
| RF-02 | El `SKILL.md` indica cuándo usarla, cómo preparar la entrada, qué ejecutar y cómo responder | Alta | MVP |
| RF-03 | Skill `resolver-sistema-lineal`: resuelve por Gauss-Jordan con fracciones exactas | Alta | MVP |
| RF-04 | La skill clasifica el sistema: solución única, infinitas (con variables libres) o sin solución | Alta | MVP |
| RF-05 | Skill `metodos-iterativos`: Jacobi y Gauss-Seidel con tolerancia y máximo de iteraciones | Alta | MVP |
| RF-06 | Los métodos iterativos entregan tabla de iteraciones, error y aviso de diagonal dominante | Alta | MVP |
| RF-07 | Los scripts devuelven JSON con el resultado y los pasos | Alta | MVP |
| RF-08 | Los scripts devuelven un mensaje de error claro ante entradas inválidas | Alta | MVP |
| RF-09 | La IA responde con un formato fijo: sistema interpretado, procedimiento, resultado y verificación | Alta | MVP |
| RF-10 | Cuando falta un dato, la IA pregunta al usuario antes de calcular | Media | MVP |
| RF-11 | Skill `regla-de-cramer`: determinante de A, determinantes de cada Ai y solución; avisa si det(A) = 0 | Alta | MVP |
| RF-12 | Skill `matriz-inversa`: inversa por Gauss-Jordan sobre [A \| I], indica si es invertible y resuelve Ax = b si se da b | Alta | MVP |
| RF-13 | **El sistema ofrece como mínimo 4 skills** y la IA elige la adecuada según la petición | Alta | MVP |
| RF-14 | Skill de verificación de solución (sustituir en cada ecuación) | Baja | Opc. |
| RF-15 | Interfaz Streamlit que llame a los mismos scripts sin IA | Baja | Opc. |
| RF-16 | Skill de sistemas no lineales (Newton multivariable) | Media | Exp. |
| RF-17 | Aplicación propia con la API de la IA y las skills | Media | Exp. |
| RF-18 | Historial de problemas resueltos | Baja | Exp. |

## 2.3 Requerimientos no funcionales

| ID | Requerimiento | Métrica | Etapa |
|----|---------------|---------|-------|
| RNF-01 | **Exactitud:** todo cálculo lo hace el script, nunca la IA | 0 operaciones aritméticas hechas por el modelo | MVP |
| RNF-02 | **Consistencia:** el mismo sistema produce siempre la misma respuesta | Resultados idénticos en 3 ejecuciones | MVP |
| RNF-03 | **Sin dependencias:** los scripts usan solo la biblioteca estándar de Python | 0 paquetes externos para ejecutarlos | MVP |
| RNF-04 | **Testabilidad:** cada script con casos felices, límite e inválidos; las skills exactas se contrastan entre sí | ≥ 35 pruebas automáticas en verde | MVP |
| RNF-05 | **Claridad:** instrucciones del `SKILL.md` cortas y sin ambigüedad | Una persona nueva las entiende en 5 minutos | MVP |
| RNF-06 | **Reutilización:** agregar una skill no obliga a modificar las demás | 1 carpeta nueva | MVP |
| RNF-07 | **Seguridad:** los scripts solo leen un JSON y no ejecutan código recibido ni acceden a la red | Revisión de código | MVP |

## 2.4 Casos de uso principales

1. **Resolver un sistema exacto:** el usuario escribe "usa la skill para resolver `2x + y − z = 8; −3x − y + 2z = −11; −2x + y + 2z = −3`". La IA lee la skill, arma `A` y `b`, ejecuta el script y responde con el procedimiento y `x = 2, y = 3, z = −1`.
2. **Detectar un sistema sin solución:** la skill indica que es incompatible y muestra la fila contradictoria.
3. **Detectar infinitas soluciones:** la skill devuelve la solución con variables libres.
4. **Aproximar con un método iterativo:** el usuario pide Gauss-Seidel con tolerancia 10⁻⁶ y recibe la tabla de iteraciones.
5. **Resolver por Cramer:** el usuario pide "resuélvelo por determinantes"; la IA elige `regla-de-cramer` y muestra det(A) y cada det(Ai).
6. **Calcular una inversa:** el usuario pide la inversa de una matriz; la IA usa `matriz-inversa` y avisa si es singular.
7. **Elegir la skill correcta:** si el usuario no nombra el método, la IA usa `resolver-sistema-lineal` por defecto.
8. **Dato faltante:** si el usuario no dice cuántas variables hay o escribe una ecuación incompleta, la IA pregunta.

## 2.5 Contrato de una skill

Toda skill debe cumplir:

- **Carpeta con nombre en minúsculas y guiones** (por ejemplo `resolver-sistema-lineal`).
- **`SKILL.md` con encabezado** que contenga `name` y `description`. La *descripción* es lo más importante: es lo que le permite a la IA decidir cuándo usar la skill.
- **Secciones del `SKILL.md`:** cuándo usar, regla principal (no calcular a mano), procedimiento paso a paso, formato de la respuesta y un ejemplo.
- **Scripts** que lean un JSON, devuelvan JSON y manejen los errores sin romperse.
- **Pruebas** automáticas en la carpeta `tests/`.

## 2.6 Riesgos

| Riesgo | Prob. | Impacto | Mitigación |
|--------|-------|---------|------------|
| La IA no activa la skill o no la lee bien | Media | Alto | Descripción precisa; batería de 24 casos para evaluar y ajustar el texto |
| La IA confunde skills parecidas (por ejemplo, Cramer, inversa y Gauss-Jordan) | Media | Medio | Cada `description` dice qué la distingue y a cuál derivar; casos de la batería que lo comprueban |
| La IA calcula a mano en lugar de ejecutar el script | Media | Alto | Regla explícita en el `SKILL.md`; revisar que el resultado coincida con el script |
| La cuenta del equipo no permite usar skills | Media | Alto | Confirmar el día 1; plan alterno (Fase 3) |
| Poca experiencia del equipo con Python | Alta | Alto | Alcance reducido, trabajo en parejas, código comentado |
| El script falla con entradas raras | Media | Medio | Pruebas con casos límite y manejo de errores |
| Los métodos iterativos no convergen | Media | Bajo | Aviso de diagonal dominante y límite de iteraciones |
| Tiempo insuficiente | Media | Alto | Elementos opcionales recortables, día de colchón |
