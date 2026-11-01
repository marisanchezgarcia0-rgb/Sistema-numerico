# Batería de evaluación (24 casos)

Se le entrega a la IA cada enunciado, **sin explicar el método** (salvo cuando el propio enunciado lo pide, como en Cramer o la inversa), con la instrucción: *«Usa la skill y resuelve»*. La IA debe elegir la skill adecuada entre las cuatro.
Las respuestas esperadas se calcularon con los propios scripts. Marcar cada columna con ✔ o ✘.

| # | Tipo | Skill esperada | Enunciado | Respuesta esperada | ¿Usó la skill? | ¿Ejecutó el script? | ¿Resultado correcto? | ¿Formato correcto? |
|---|------|----------------|-----------|--------------------|----|----|----|----|
| 1 | Única 2x2 | resolver-sistema-lineal | x1 + x2 = 3; x1 - x2 = 1 | unica: x1 = 2; x2 = 1 |  |  |  |  |
| 2 | Única 2x2 | resolver-sistema-lineal | 2*x1 + 3*x2 = 8; 4*x1 - x2 = 2 | unica: x1 = 1; x2 = 2 |  |  |  |  |
| 3 | Única 3x3 | resolver-sistema-lineal | 2*x1 + x2 - x3 = 8; -3*x1 - x2 + 2*x3 = -11; -2*x1 + x2 + 2*x3 = -3 | unica: x1 = 2; x2 = 3; x3 = -1 |  |  |  |  |
| 4 | Única 3x3 | resolver-sistema-lineal | x1 + x2 + x3 = 6; 2*x2 + 5*x3 = -4; 2*x1 + 5*x2 - x3 = 27 | unica: x1 = 5; x2 = 3; x3 = -2 |  |  |  |  |
| 5 | Única 3x3 | resolver-sistema-lineal | 3*x1 + 2*x2 - x3 = 1; 2*x1 - 2*x2 + 4*x3 = -2; -x1 + 0.5*x2 - x3 = 0 | unica: x1 = 1; x2 = -2; x3 = -2 |  |  |  |  |
| 6 | Única 4x4 | resolver-sistema-lineal | x1 + x2 = 3; x2 + x3 = 5; x3 + x4 = 7; x1 + 2*x4 = 9 | unica: x1 = 1; x2 = 2; x3 = 3; x4 = 4 |  |  |  |  |
| 7 | Fracciones | resolver-sistema-lineal | 1/2*x1 + 1/3*x2 = 2; x1 + x2 = 3 | unica: x1 = 6; x2 = -3 |  |  |  |  |
| 8 | Decimales | resolver-sistema-lineal | 0.5*x1 + 1.5*x2 = 3; 2*x1 - x2 = 1 | unica: x1 = 9/7; x2 = 11/7 |  |  |  |  |
| 9 | Fracciones | resolver-sistema-lineal | 3*x1 + x2 = 1; x1 + 2*x2 = 1 | unica: x1 = 1/5; x2 = 2/5 |  |  |  |  |
| 10 | Pivote cero | resolver-sistema-lineal | x2 = 2; x1 + x2 = 3 | unica: x1 = 1; x2 = 2 |  |  |  |  |
| 11 | Pivote cero | resolver-sistema-lineal | 2*x2 + x3 = 4; x1 + x2 + x3 = 6; 2*x1 + x2 = 5 | unica: x1 = 7/3; x2 = 1/3; x3 = 10/3 |  |  |  |  |
| 12 | Infinitas | resolver-sistema-lineal | x1 + 2*x2 = 3; 2*x1 + 4*x2 = 6 | infinitas: x1 = 3 + (-2)*x2; x2 = libre |  |  |  |  |
| 13 | Infinitas | resolver-sistema-lineal | x1 + x2 + x3 = 3; x1 - x2 = 1 | infinitas: x1 = 2 + (-1/2)*x3; x2 = 1 + (-1/2)*x3; x3 = libre |  |  |  |  |
| 14 | Sin solución | resolver-sistema-lineal | x1 + 2*x2 = 3; 2*x1 + 4*x2 = 7 | sin_solucion |  |  |  |  |
| 15 | Sin solución | resolver-sistema-lineal | x1 + x2 = 1; x1 + x2 = 2; x1 + 2*x2 = 3 | sin_solucion |  |  |  |  |
| 16 | Dato faltante | resolver-sistema-lineal | 2x + y = 5; x - = 1  (ecuación incompleta) | La IA debe PREGUNTAR, no calcular |  |  |  |  |
| 17 | Dato faltante | resolver-sistema-lineal | Resuelve el sistema de las 3 ecuaciones (sin escribirlas) | La IA debe PEDIR las ecuaciones |  |  |  |  |
| 18 | Jacobi | metodos-iterativos | 4*x1 + x2 + x3 = 6; x1 + 5*x2 + 2*x3 = 8; x1 + 2*x2 + 6*x3 = 9  / método jacobi, tolerancia 1e-6 | convergió en 24 iter: x1 = 0.9999997; x2 = 0.99999966; x3 = 0.9999997 |  |  |  |  |
| 19 | Gauss-Seidel | metodos-iterativos | 10*x1 + 2*x2 + x3 = 7; x1 + 5*x2 + x3 = -8; 2*x1 + 3*x2 + 10*x3 = 6  / método gauss_seidel, tolerancia 1e-6 | convergió en 8 iter: x1 = 0.99999999; x2 = -2; x3 = 1 |  |  |  |  |
| 20 | No converge | metodos-iterativos | x1 + 3*x2 = 4; 4*x1 + x2 = 5  / método jacobi, tolerancia 1e-6 | no converge (diagonal no dominante) |  |  |  |  |
| 21 | Cramer | regla-de-cramer | Resuelve por Cramer: 2*x1 + x2 - x3 = 8; -3*x1 - x2 + 2*x3 = -11; -2*x1 + x2 + 2*x3 = -3 | det(A) = -1; x1 = 2; x2 = 3; x3 = -1 |  |  |  |  |
| 22 | Cramer con det = 0 | regla-de-cramer | Resuelve por determinantes: x1 + 2*x2 = 3; 2*x1 + 4*x2 = 6 | det(A) = 0: Cramer no aplica; la IA debe sugerir resolver-sistema-lineal |  |  |  |  |
| 23 | Matriz inversa | matriz-inversa | Calcula la inversa de [[2,1],[5,3]] y úsala para resolver con b = [1, 2] | inversa [[3,-1],[-5,2]], det = 1; x1 = 1; x2 = -1 |  |  |  |  |
| 24 | Inversa singular | matriz-inversa | ¿Es invertible la matriz [[1,2],[2,4]]? Calcula su inversa | No es invertible (det = 0); la IA debe sugerir resolver-sistema-lineal |  |  |  |  |


**Meta (Hito 2):** al menos 22 de 24 casos con las 4 columnas en ✔ (90 %).

Nota: en los casos de «dato faltante» lo correcto es que la IA pregunte; ahí «¿Ejecutó el script?» debe ser ✘.
