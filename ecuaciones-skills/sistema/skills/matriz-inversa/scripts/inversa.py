#!/usr/bin/env python3
"""Calcula la inversa de A por Gauss-Jordan sobre [A | I] y, si se da b, resuelve x = A^-1 b.

Uso:  python inversa.py entrada.json
Entrada JSON:  {"A": [[2,1],[5,3]], "b": [1,2]}     ("b" es opcional; A debe ser cuadrada)
Salida JSON:   {"ok": true, "invertible": true|false, "determinante": "...",
                "inversa": [[...]], "solucion": [...], "pasos": [...]}
"""
import json
import sys
from fractions import Fraction


def a_fraccion(x) -> Fraction:
    try:
        return Fraction(str(x).strip())
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"Numero no valido: {x!r}")


def fmt(M) -> str:
    return " ; ".join("[" + ", ".join(str(v) for v in f) + "]" for f in M)


def resolver(A, b=None) -> dict:
    if not A or not isinstance(A, list) or not all(isinstance(f, list) for f in A):
        raise ValueError("A debe ser una lista de filas (lista de listas)")
    n = len(A)
    if any(len(f) != n for f in A):
        raise ValueError("Solo las matrices cuadradas (n x n) pueden tener inversa")
    if b is not None and len(b) != n:
        raise ValueError(f"b debe tener {n} elementos y tiene {len(b)}")
    M = [[a_fraccion(v) for v in f] + [Fraction(int(i == j)) for j in range(n)] for i, f in enumerate(A)]
    pasos = [f"Matriz ampliada [A | I]: {fmt(M)}"]
    det = Fraction(1)
    for col in range(n):
        p = next((r for r in range(col, n) if M[r][col] != 0), None)
        if p is None:
            pasos.append(f"Columna {col + 1} sin pivote: la matriz es singular.")
            return {"ok": True, "invertible": False, "determinante": "0", "inversa": [], "solucion": [],
                    "pasos": pasos,
                    "explicacion": "det(A) = 0: la matriz no es invertible. Use la skill "
                                   "resolver-sistema-lineal para analizar el sistema."}
        if p != col:
            M[col], M[p] = M[p], M[col]
            det = -det
            pasos.append(f"Intercambiar F{col + 1} <-> F{p + 1}")
        piv = M[col][col]
        det *= piv
        if piv != 1:
            M[col] = [v / piv for v in M[col]]
            pasos.append(f"F{col + 1} = F{col + 1} / ({piv})")
        for r in range(n):
            if r != col and M[r][col] != 0:
                k = M[r][col]
                M[r] = [a - k * c for a, c in zip(M[r], M[col])]
                pasos.append(f"F{r + 1} = F{r + 1} - ({k}) * F{col + 1}")
        pasos.append(f"Matriz tras la columna {col + 1}: {fmt(M)}")
    inv = [fila[n:] for fila in M]
    pasos.append(f"A^-1 = {fmt(inv)}")
    salida = {"ok": True, "invertible": True, "determinante": str(det),
              "inversa": [[str(v) for v in f] for f in inv], "solucion": [], "pasos": pasos,
              "explicacion": f"A es invertible (det(A) = {det})."}
    if b is not None:
        bv = [a_fraccion(v) for v in b]
        x = [sum(inv[i][j] * bv[j] for j in range(n)) for i in range(n)]
        salida["solucion"] = [f"x{i + 1} = {v}" for i, v in enumerate(x)]
        pasos.append("x = A^-1 * b = " + ", ".join(str(v) for v in x))
        salida["explicacion"] += " Solucion de Ax = b: " + ", ".join(salida["solucion"]) + "."
    return salida


def main() -> int:
    try:
        texto = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
        d = json.loads(texto)
        salida = resolver(d["A"], d.get("b"))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
        salida = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(salida, ensure_ascii=False, indent=2))
    return 0 if salida.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
