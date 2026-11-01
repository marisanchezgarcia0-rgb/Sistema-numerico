# Fase 1 — Planteamiento del problema

## 1.1 Contexto

Resolver sistemas de ecuaciones es una tarea que se repite constantemente en matemáticas, ingeniería y programación. Cada vez que alguien le pide ayuda a una IA, debe volver a explicarle qué método usar, en qué formato dar los datos, cómo mostrar el procedimiento y qué verificar. Esa solicitud se repite una y otra vez, y el resultado cambia de una conversación a otra.

## 1.2 Problemática

| # | Problema detectado | Consecuencia |
|---|--------------------|--------------|
| P1 | El usuario debe repetir las mismas instrucciones en cada solicitud | Pérdida de tiempo y esfuerzo |
| P2 | La respuesta de la IA varía en formato y nivel de detalle entre conversaciones | Resultados inconsistentes |
| P3 | Un modelo de lenguaje puede equivocarse al hacer aritmética (sobre todo con fracciones o sistemas grandes) | Soluciones incorrectas presentadas con seguridad |
| P4 | No hay una forma estándar de saber si un sistema tiene solución única, infinitas o ninguna | Casos especiales mal resueltos |
| P5 | Las instrucciones quedan perdidas en el historial de cada chat | No se pueden compartir, mejorar ni reutilizar |

## 1.3 Pregunta de investigación

¿Cómo diseñar, en dos semanas, un conjunto de *skills* para resolver sistemas de ecuaciones de modo que el usuario solo entregue el sistema y le indique a la IA que lea la skill, y esta lo resuelva siempre con el mismo método, el mismo formato y cálculo exacto?

## 1.4 Qué es una skill en este proyecto

Una **skill** es una carpeta reutilizable que contiene:

- Un archivo **`SKILL.md`** con instrucciones para la IA: cuándo usarla, cómo interpretar el problema, qué comando ejecutar, cómo leer el resultado y en qué formato responder.
- Una carpeta **`scripts/`** con código Python que hace el cálculo de forma exacta y determinista.

El usuario no vuelve a explicar el método: le dice a la IA "usa la skill para resolver este sistema" y le entrega las ecuaciones.

> **Principio clave:** la IA lee, interpreta y explica; el script de Python calcula. Así se evitan los errores aritméticos del modelo (P3).

## 1.5 Solución propuesta

Un conjunto de skills de sistemas de ecuaciones, probadas con pruebas automáticas, que una IA (Claude) puede leer y ejecutar. El proyecto se entrega en dos etapas:

- **Etapa 1 — MVP (2 semanas):** **4 skills** completas (`resolver-sistema-lineal`, `metodos-iterativos`, `regla-de-cramer` y `matriz-inversa`), con scripts probados y una batería de casos de evaluación con la IA.
- **Etapa 2 — Expansión:** más skills (Cramer, matriz inversa, sistemas no lineales), interfaz web propia, aplicación con la API de la IA y más funciones.

## 1.6 Objetivos

**General:** desarrollar en dos semanas un conjunto de skills de sistemas de ecuaciones que una IA pueda leer y ejecutar para resolver problemas repetitivos con resultados consistentes y correctos.

**Específicos:**

1. Definir una estructura estándar de skill (`SKILL.md` + `scripts/`).
2. Implementar la skill `resolver-sistema-lineal` (Gauss-Jordan) con clasificación del sistema (única, infinitas o sin solución).
3. Implementar la skill `metodos-iterativos` (Jacobi y Gauss-Seidel) con tabla de iteraciones.
4. Implementar la skill `regla-de-cramer` con el determinante de A y de cada matriz modificada.
5. Implementar la skill `matriz-inversa` (Gauss-Jordan sobre [A | I]), con resolución opcional de Ax = b.
6. Garantizar el cálculo exacto mediante scripts de Python con pruebas automáticas.
7. Evaluar con la IA que lee correctamente cada skill y que elige la adecuada entre las cuatro, usando una batería de al menos 24 sistemas.
8. Documentar el proyecto para que sea reutilizable y ampliable.

## 1.7 Alcance

**Incluido en el MVP**

- Sistemas lineales de cualquier tamaño: n×n y también con más o menos ecuaciones que incógnitas.
- Entrada con enteros, decimales y fracciones.
- Cuatro skills: Gauss-Jordan (solución exacta con fracciones), Jacobi y Gauss-Seidel, regla de Cramer y matriz inversa.
- Procedimiento paso a paso y manejo claro de errores.
- Pruebas automáticas de los scripts.

**Opcional dentro de las 2 semanas** (solo si se cumple el Hito 2)

- Una quinta skill: verificación de una solución (comprobar que cumple todas las ecuaciones).
- Interfaz mínima en Streamlit que llame a los mismos scripts.

**Etapa 2 (fuera del plazo)**

- Sistemas no lineales (Newton multivariable) y descomposición LU.
- Aplicación propia con la API de la IA.
- Historial, base de datos y frontend avanzado.
- Reconocimiento de sistemas desde una foto.

## 1.8 Restricciones y supuestos

- Plazo total: **2 semanas** (10 días hábiles).
- Lenguaje obligatorio: **Python**.
- Equipo con poca experiencia: se prioriza entender sobre acumular funciones.
- Se asume que el equipo tiene acceso a una IA capaz de usar skills. **Esto debe confirmarse el día 1**, porque la disponibilidad de skills depende del plan y del producto que se use. Si no estuviera disponible, aplica el plan alterno descrito en la Fase 3.

## 1.9 Criterios de éxito

- Las cuatro skills resuelven correctamente el 100 % de los casos de prueba automáticos.
- **El sistema tiene como mínimo 4 skills operativas.**
- La IA, al leer las skills, elige la adecuada y resuelve correctamente al menos el 90 % de la batería de 24 sistemas.
- El usuario solo escribe el sistema y la instrucción de usar la skill; no repite el método.
- Cada respuesta incluye el procedimiento y el tipo de sistema.
- Cada integrante puede explicar cómo funciona al menos una skill.
