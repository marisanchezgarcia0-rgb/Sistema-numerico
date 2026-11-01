#!/usr/bin/env python3
"""Resuelve un sistema lineal cuadrado Ax = b con la regla de Cramer (aritmetica exacta).

Uso:  python cramer.py entrada.json
Entrada JSON:  {"A": [[2,1],[1,-1]], "b": [5,1]}   (A debe ser cuadrada)
Salida JSON:   {"ok": true, "tipo": "unica|no_aplicable", "determinante": "...",
                "determinantes_variables": {...}, "solucion": [...], "pasos": [...]}
"""
import json
import sys
from fractions import Fraction


def a_fraccion(x) -> Fraction:
    try:
        return Fraction(str(x).strip())
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"Numero no valido: {x!r}")


def determinante(M) -> Fraction:
    """Determinante por eliminacion (exacto, con Fraction)."""
    M = [fila[:] for fila in M]
    n = len(M)
    det = Fraction(1)
    for col in range(n):
        p = next((r for r in range(col, n) if M[r][col] != 0), None)
        if p is None:
            return Fraction(0)
        if p != col:
            M[col], M[p] = M[p], M[col]
            det = -det
        det *= M[col][col]
        for r in range(col + 1, n):
            k = M[r][col] / M[col][col]
            M[r] = [a - k * c for a, c in zip(M[r], M[col])]
    return det


def fmt(M) -> str:
    return " ; ".join("[" + ", ".join(str(v) for v in f) + "]" for f in M)


def resolver(A, b) -> dict:
    if not A or not isinstance(A, list) or not all(isinstance(f, list) for f in A):
        raise ValueError("A debe ser una lista de filas (lista de listas)")
    n = len(A)
    if any(len(f) != n for f in A):
        raise ValueError("La regla de Cramer requiere una matriz A cuadrada (n x n)")
    if len(b) != n:
        raise ValueError(f"b debe tener {n} elementos y tiene {len(b)}")
    A = [[a_fraccion(v) for v in f] for f in A]
    b = [a_fraccion(v) for v in b]

    d = determinante(A)
    pasos = [f"Matriz A: {fmt(A)}", f"det(A) = {d}"]
    if d == 0:
        pasos.append("Como det(A) = 0, la regla de Cramer no se puede aplicar.")
        return {"ok": True, "tipo": "no_aplicable", "determinante": str(d), "determinantes_variables": {},
                "solucion": [], "pasos": pasos,
                "explicacion": "det(A) = 0: no hay solucion unica. Use la skill resolver-sistema-lineal "
                               "para saber si tiene infinitas soluciones o ninguna."}
    dets, sol = {}, []
    for i in range(n):
        Ai = [fila[:i] + [b[r]] + fila[i + 1:] for r, fila in enumerate(A)]
        di = determinante(Ai)
        dets[f"det(A{i + 1})"] = str(di)
        pasos.append(f"A{i + 1} = A con la columna {i + 1} reemplazada por b: {fmt(Ai)}")
        pasos.append(f"det(A{i + 1}) = {di}")
        xi = di / d
        pasos.append(f"x{i + 1} = det(A{i + 1}) / det(A) = {di} / {d} = {xi}")
        sol.append(f"x{i + 1} = {xi}")
    return {"ok": True, "tipo": "unica", "determinante": str(d), "determinantes_variables": dets,
            "solucion": sol, "pasos": pasos,
            "explicacion": "Solucion unica por Cramer: " + ", ".join(sol) + "."}


def main() -> int:
    try:
        texto = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
        d = json.loads(texto)
        salida = resolver(d["A"], d["b"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
        salida = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(salida, ensure_ascii=False, indent=2))
    return 0 if salida.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
