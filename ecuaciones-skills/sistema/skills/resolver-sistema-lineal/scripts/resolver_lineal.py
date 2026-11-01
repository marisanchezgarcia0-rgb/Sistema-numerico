#!/usr/bin/env python3
"""Resuelve un sistema lineal Ax = b por Gauss-Jordan con aritmetica exacta.

Uso:  python resolver_lineal.py entrada.json
      (o por entrada estandar:  cat entrada.json | python resolver_lineal.py)

Entrada JSON:  {"A": [[2,1],[1,-1]], "b": [5,1]}
  Los numeros pueden ser enteros, decimales o fracciones como texto: "1/3".
Salida JSON:   {"ok": true, "tipo": "unica|infinitas|sin_solucion",
                "solucion": [...], "pasos": [...], "explicacion": "..."}
"""
import json
import sys
from fractions import Fraction


def a_fraccion(x) -> Fraction:
    try:
        return Fraction(str(x).strip())
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"Numero no valido: {x!r}")


def fmt_matriz(M) -> str:
    return " ; ".join("[" + ", ".join(str(v) for v in fila) + "]" for fila in M)


def resolver(A, b) -> dict:
    if not A or not isinstance(A, list) or not all(isinstance(f, list) for f in A):
        raise ValueError("A debe ser una lista de filas (lista de listas)")
    m, n = len(A), len(A[0])
    if n == 0 or any(len(f) != n for f in A):
        raise ValueError("Todas las filas de A deben tener la misma cantidad de columnas")
    if len(b) != m:
        raise ValueError(f"b debe tener {m} elementos (uno por ecuacion) y tiene {len(b)}")

    M = [[a_fraccion(v) for v in fila] + [a_fraccion(bi)] for fila, bi in zip(A, b)]
    pasos = [f"Matriz aumentada [A|b]: {fmt_matriz(M)}"]
    pivotes = []  # columna de cada pivote
    fila = 0
    for col in range(n):
        if fila >= m:
            break
        p = next((r for r in range(fila, m) if M[r][col] != 0), None)
        if p is None:
            pasos.append(f"Columna {col + 1}: sin pivote (x{col + 1} sera variable libre)")
            continue
        if p != fila:
            M[fila], M[p] = M[p], M[fila]
            pasos.append(f"Intercambiar F{fila + 1} <-> F{p + 1}")
        pivote = M[fila][col]
        if pivote != 1:
            M[fila] = [v / pivote for v in M[fila]]
            pasos.append(f"F{fila + 1} = F{fila + 1} / ({pivote})")
        for r in range(m):
            if r != fila and M[r][col] != 0:
                k = M[r][col]
                M[r] = [a - k * c for a, c in zip(M[r], M[fila])]
                pasos.append(f"F{r + 1} = F{r + 1} - ({k}) * F{fila + 1}")
        pivotes.append(col)
        pasos.append(f"Matriz tras la columna {col + 1}: {fmt_matriz(M)}")
        fila += 1

    # Inconsistencia: fila con todos los coeficientes en 0 pero termino independiente distinto de 0
    for r in range(m):
        if all(v == 0 for v in M[r][:n]) and M[r][n] != 0:
            pasos.append(f"F{r + 1} queda 0 = {M[r][n]}: contradiccion")
            return {"ok": True, "tipo": "sin_solucion", "solucion": [], "pasos": pasos,
                    "explicacion": "El sistema es incompatible: no tiene solucion."}

    libres = [c for c in range(n) if c not in pivotes]
    if not libres:
        sol = [f"x{c + 1} = {M[i][n]}" for i, c in enumerate(pivotes)]
        return {"ok": True, "tipo": "unica", "solucion": sol, "pasos": pasos,
                "explicacion": "El sistema tiene solucion unica: " + ", ".join(sol) + "."}

    sol = []
    for i, c in enumerate(pivotes):
        partes = [f"{M[i][n]}"] if M[i][n] != 0 else []
        for l in libres:
            coef = -M[i][l]
            if coef != 0:
                partes.append(f"({coef})*x{l + 1}")
        sol.append(f"x{c + 1} = " + (" + ".join(partes) if partes else "0"))
    sol += [f"x{l + 1} = libre" for l in libres]
    return {"ok": True, "tipo": "infinitas", "solucion": sol, "pasos": pasos,
            "explicacion": f"Infinitas soluciones con {len(libres)} variable(s) libre(s)."}


def main() -> int:
    try:
        texto = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
        datos = json.loads(texto)
        salida = resolver(datos["A"], datos["b"])
    except (ValueError, KeyError, json.JSONDecodeError, OSError) as exc:
        salida = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(salida, ensure_ascii=False, indent=2))
    return 0 if salida.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
