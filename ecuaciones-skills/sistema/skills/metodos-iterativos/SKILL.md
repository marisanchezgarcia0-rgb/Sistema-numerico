---
name: metodos-iterativos
description: Resuelve sistemas de ecuaciones lineales con los metodos iterativos de Jacobi o Gauss-Seidel y muestra la tabla de iteraciones y el error. Usar cuando el usuario pida Jacobi, Gauss-Seidel, un metodo iterativo, una aproximacion con tolerancia, o quiera ver como converge un sistema.
---

# Metodos iterativos (Jacobi y Gauss-Seidel)

## Cuando usar esta skill
- El usuario nombra Jacobi o Gauss-Seidel, o pide una solucion aproximada con una tolerancia.
- Quiere ver la tabla de iteraciones o comprobar si el metodo converge.

Si el usuario solo quiere la solucion exacta, usa la skill `resolver-sistema-lineal`.

## Regla principal
**No iteres a mano.** Ejecuta siempre el script y explica su resultado.

## Procedimiento

> **Herramienta o script:** si tu entorno ofrece la herramienta `resolver_iterativo`, llamala con `A`, `b`, `metodo`, `x0`, `tolerancia` y `max_iter` (cada numero como texto: "2", "-1.5" o "1/3") en lugar de crear el JSON y ejecutar el script; el resultado es el mismo. Si no hay herramienta, sigue los pasos con el script.

1. Pasa el sistema a `A` (cuadrada, n x n) y `b`.
2. Define los parametros. Si el usuario no los da, usa estos y dilo en la respuesta:
   - `metodo`: `gauss_seidel`
   - `x0`: vector de ceros
   - `tolerancia`: `1e-6`
   - `max_iter`: `100`
3. Crea el JSON:
   ```json
   {"A": [[4,1,1],[1,5,2],[1,2,6]], "b": [6,8,9], "metodo": "gauss_seidel", "x0": [0,0,0], "tolerancia": 1e-8, "max_iter": 100}
   ```
4. Ejecuta: `python scripts/iterativos.py entrada.json`
5. Interpreta la salida:
   - `convergio: true`: da la solucion y el numero de iteraciones.
   - `convergio: false`: explica que no converge y por que (revisa `diagonal_dominante`).
   - Si hay un cero en la diagonal, el script lo indica: sugiere reordenar las ecuaciones.
   - Si `pasos` trae un aviso de diagonal no dominante, mencionalo.
6. Si `ok` es `false`, muestra el error en palabras sencillas.

## Formato de la respuesta al usuario
1. **Metodo y parametros usados.**
2. **Tabla de iteraciones** (iteracion, valores de x, error); si son muchas, muestra las primeras y las ultimas.
3. **Resultado** y si convergio.
4. **Comentario** sobre la diagonal dominante y la convergencia.
