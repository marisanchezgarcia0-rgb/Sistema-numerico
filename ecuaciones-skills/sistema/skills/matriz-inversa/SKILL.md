---
name: matriz-inversa
description: Calcula la matriz inversa de una matriz cuadrada por Gauss-Jordan sobre [A | I], indica si es invertible y, si se da el vector b, resuelve Ax = b con x = A^-1 b. Usar cuando el usuario pida la inversa de una matriz, quiera saber si una matriz es invertible o pida resolver un sistema "con la matriz inversa".
---

# Matriz inversa

## Cuando usar esta skill
- El usuario pide la inversa de una matriz o saber si es invertible.
- Pide resolver un sistema usando la inversa (`x = A^-1 b`).

Solo aplica a matrices cuadradas. Para resolver un sistema sin pedir la inversa, usar `resolver-sistema-lineal`.

## Regla principal
**No inviertas la matriz a mano.** Ejecuta siempre el script.

## Procedimiento

> **Herramienta o script:** si tu entorno ofrece la herramienta `calcular_inversa`, llamala con `A` (y `b` si se da` (cada numero como texto: "2", "-1.5" o "1/3") en lugar de crear el JSON y ejecutar el script; el resultado es el mismo. Si no hay herramienta, sigue los pasos con el script.

1. Obtiene `A` (cuadrada, una fila por lista). Si el usuario tambien da un sistema, obtiene `b`.
2. Si algun dato falta o es ambiguo, **pregunta al usuario**.
3. Crea el JSON (`b` es opcional):
   ```json
   {"A": [[2, 1], [5, 3]], "b": [1, 2]}
   ```
4. Ejecuta: `python scripts/inversa.py entrada.json`
5. Lee el resultado:
   - `invertible: true`: muestra `inversa`, `determinante` y, si hay `b`, la `solucion`.
   - `invertible: false`: explica que la matriz es singular (det = 0) y ofrece usar `resolver-sistema-lineal`.
6. Si `ok` es `false`, explica el error en palabras sencillas.

## Formato de la respuesta al usuario
1. **Matriz interpretada.**
2. **Procedimiento:** operaciones entre filas sobre `[A | I]` (resumidas si son muchas).
3. **Resultado:** la inversa y el determinante, o la indicacion de que no es invertible.
4. **Solucion del sistema** (si se dio `b`) y **verificacion**: comprobar que `A * A^-1 = I` en alguna fila.

## Ejemplo
`A = [[2,1],[5,3]]` -> inversa `[[3, -1], [-5, 2]]`, `det(A) = 1`.
