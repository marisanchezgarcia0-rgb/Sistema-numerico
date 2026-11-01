---
name: resolver-sistema-lineal
description: Resuelve sistemas de ecuaciones lineales (Ax = b) por el metodo de Gauss-Jordan con aritmetica exacta y muestra el procedimiento paso a paso. Usar cuando el usuario pida resolver, clasificar o explicar un sistema de ecuaciones lineales (2x2, 3x3 o mayor), o diga cosas como "resuelve este sistema", "usa el metodo de Gauss-Jordan" o "dime si tiene solucion".
---

# Resolver sistema lineal (Gauss-Jordan)

## Cuando usar esta skill
- El usuario entrega ecuaciones lineales, por ejemplo `2x + y - z = 8`, o una matriz aumentada.
- Quiere la solucion, el procedimiento o saber si el sistema tiene solucion unica, infinitas o ninguna.

No usar para ecuaciones no lineales (x^2, sin(x), etc.): avisar al usuario de que esta skill no las cubre.

## Regla principal
**No hagas la aritmetica tu mismo.** Siempre ejecuta el script; solo traduces el enunciado y explicas el resultado.

## Procedimiento

> **Herramienta o script:** si tu entorno ofrece la herramienta `resolver_lineal`, llamala con `A` y `b` (cada numero como texto: "2", "-1.5" o "1/3") en lugar de crear el JSON y ejecutar el script; el resultado es el mismo. Si no hay herramienta, sigue los pasos con el script.

1. Pasa las ecuaciones a forma matricial: `A` (coeficientes, una fila por ecuacion, una columna por variable, en el orden x1, x2, ...) y `b` (terminos independientes). Si falta una variable en una ecuacion, su coeficiente es 0.
2. Si hay un dato ambiguo o faltante, **pregunta al usuario** antes de ejecutar.
3. Crea un archivo JSON con este formato:
   ```json
   {"A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], "b": [8, -11, -3]}
   ```
   Se aceptan enteros, decimales y fracciones como texto (`"1/3"`).
4. Ejecuta: `python scripts/resolver_lineal.py entrada.json`
5. Lee el JSON de salida y responde segun `tipo`:
   - `unica`: da la solucion y explica los pasos principales.
   - `infinitas`: da la solucion parametrica e indica las variables libres.
   - `sin_solucion`: explica que el sistema es incompatible y muestra la fila que lo prueba.
6. Si `ok` es `false`, muestra el mensaje de `error` en palabras sencillas y pide corregir el dato.

## Formato de la respuesta al usuario
1. **Sistema interpretado:** las ecuaciones y la matriz `[A|b]`.
2. **Procedimiento:** los pasos del campo `pasos`, resumidos si son muchos.
3. **Resultado:** la solucion y el tipo de sistema.
4. **Verificacion:** sustituye la solucion en una ecuacion original (solo si el tipo es `unica`).

## Ejemplo
Entrada del usuario: "Resuelve 2x + y - z = 8, -3x - y + 2z = -11, -2x + y + 2z = -3"
Resultado esperado: `x1 = 2, x2 = 3, x3 = -1` (solucion unica).
