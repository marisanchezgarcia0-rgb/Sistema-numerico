#!/usr/bin/env python3
"""Resuelve Ax = b con Jacobi o Gauss-Seidel y devuelve la tabla de iteraciones.

Uso:  python iterativos.py entrada.json
Entrada JSON:
  {"A": [[4,1],[2,5]], "b": [9,13], "metodo": "jacobi" | "gauss_seidel",
   "x0": [0,0], "tolerancia": 1e-6, "max_iter": 100}
  (x0, tolerancia y max_iter son opcionales)
"""
import json
import sys


def resolver(A, b, metodo="gauss_seidel", x0=None, tolerancia=1e-6, max_iter=100) -> dict:
    n = len(A)
    if n == 0 or any(len(f) != n for f in A):
        raise ValueError("A debe ser una matriz cuadrada")
    if len(b) != n:
        raise ValueError(f"b debe tener {n} elementos")
    if metodo not in ("jacobi", "gauss_seidel"):
        raise ValueError("metodo debe ser 'jacobi' o 'gauss_seidel'")
    if tolerancia <= 0 or max_iter < 1:
        raise ValueError("tolerancia debe ser > 0 y max_iter >= 1")
    A = [[float(v) for v in f] for f in A]
    b = [float(v) for v in b]
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError(f"A[{i + 1}][{i + 1}] = 0: reordene las ecuaciones para evitar ceros en la diagonal")
    x = [float(v) for v in x0] if x0 else [0.0] * n
    if len(x) != n:
        raise ValueError(f"x0 debe tener {n} elementos")

    dominante = all(abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i) for i in range(n))
    pasos = []
    if not dominante:
        pasos.append("Aviso: la matriz NO es estrictamente diagonal dominante; la convergencia no esta garantizada.")
    tabla = []
    for k in range(1, max_iter + 1):
        previo = x[:]
        nuevo = x[:] if metodo == "gauss_seidel" else [0.0] * n
        for i in range(n):
            fuente = previo if metodo == "jacobi" else nuevo
            s = sum(A[i][j] * fuente[j] for j in range(n) if j != i)
            nuevo[i] = (b[i] - s) / A[i][i]
        x = nuevo
        error = max(abs(a - c) for a, c in zip(x, previo))
        tabla.append({"iter": k, "x": [round(v, 8) for v in x], "error": error})
        if error < tolerancia:
            sol = [f"x{i + 1} = {v:.8g}" for i, v in enumerate(x)]
            return {"ok": True, "convergio": True, "iteraciones": k, "solucion": sol, "tabla": tabla,
                    "pasos": pasos, "diagonal_dominante": dominante,
                    "explicacion": f"Convergio en {k} iteraciones: " + ", ".join(sol) + "."}
        if any(abs(v) > 1e150 for v in x):
            break
    return {"ok": True, "convergio": False, "iteraciones": len(tabla), "solucion": [], "tabla": tabla[-5:],
            "pasos": pasos, "diagonal_dominante": dominante,
            "explicacion": "No convergio (el metodo diverge o se agotaron las iteraciones)."}


def main() -> int:
    try:
        texto = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
        d = json.loads(texto)
        salida = resolver(d["A"], d["b"], d.get("metodo", "gauss_seidel"), d.get("x0"),
                          d.get("tolerancia", 1e-6), d.get("max_iter", 100))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
        salida = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(salida, ensure_ascii=False, indent=2))
    return 0 if salida.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
