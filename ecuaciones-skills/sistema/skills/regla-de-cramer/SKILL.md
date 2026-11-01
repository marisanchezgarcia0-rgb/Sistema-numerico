---
name: regla-de-cramer
description: Resuelve sistemas de ecuaciones lineales cuadrados (n x n) con la regla de Cramer, mostrando el determinante de A y el de cada matriz modificada. Usar cuando el usuario pida explicitamente "regla de Cramer", "por determinantes", o quiera ver los determinantes del sistema.
---

# Regla de Cramer

## Cuando usar esta skill
- El usuario nombra la regla de Cramer o pide resolver "por determinantes".
- El sistema tiene tantas ecuaciones como incognitas (n x n).

Si el sistema no es cuadrado o el usuario no pide un metodo concreto, usar `resolver-sistema-lineal`.

## Regla principal
**No calcules determinantes a mano.** Ejecuta siempre el script.

## Procedimiento

> **Herramienta o script:** si tu entorno ofrece la herramienta `resolver_cramer`, llamala con `A` y `b` (cada numero como texto: "2", "-1.5" o "1/3") en lugar de crear el JSON y ejecutar el script; el resultado es el mismo. Si no hay herramienta, sigue los pasos con el script.

1. Pasa el sistema a `A` (coeficientes, una fila por ecuacion, columnas en el orden x1, x2, ...) y `b`. Si una variable no aparece, su coeficiente es 0.
2. Si algun dato es ambiguo o falta, **pregunta al usuario**.
3. Crea el JSON:
   ```json
   {"A": [[2, 1], [1, -1]], "b": [5, 1]}
   ```
4. Ejecuta: `python scripts/cramer.py entrada.json`
5. Lee el resultado segun `tipo`:
   - `unica`: muestra `det(A)`, cada `det(Ai)` y las divisiones `xi = det(Ai) / det(A)`.
   - `no_aplicable`: `det(A) = 0`; explica que Cramer no sirve y ofrece usar `resolver-sistema-lineal`.
6. Si `ok` es `false`, muestra el error en palabras sencillas (por ejemplo, "la matriz no es cuadrada").

## Formato de la respuesta al usuario
1. **Sistema interpretado** y matriz `A`.
2. **Determinante de A.**
3. **Matrices Ai y sus determinantes** (una por variable).
4. **Resultado:** `xi = det(Ai) / det(A)`.
5. **Verificacion** sustituyendo en una ecuacion original (si hay solucion).

## Ejemplo
"Resuelve por Cramer: x + y = 3; x - y = 1" -> `det(A) = -2`, `x1 = 2`, `x2 = 1`.
