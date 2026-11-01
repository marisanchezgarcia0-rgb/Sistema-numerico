"""Pruebas de los scripts de las skills. Ejecutar:  pytest"""
import importlib.util
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]


def cargar(ruta: str):
    spec = importlib.util.spec_from_file_location(Path(ruta).stem, RAIZ / ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lineal = cargar("skills/resolver-sistema-lineal/scripts/resolver_lineal.py")
iter_ = cargar("skills/metodos-iterativos/scripts/iterativos.py")
cramer = cargar("skills/regla-de-cramer/scripts/cramer.py")
inversa = cargar("skills/matriz-inversa/scripts/inversa.py")


# ---------------- Gauss-Jordan ----------------
def test_unica_2x2():
    r = lineal.resolver([[1, 1], [1, -1]], [3, 1])
    assert r["tipo"] == "unica" and r["solucion"] == ["x1 = 2", "x2 = 1"]


def test_unica_3x3():
    r = lineal.resolver([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])
    assert r["solucion"] == ["x1 = 2", "x2 = 3", "x3 = -1"]


def test_fracciones_exactas():
    r = lineal.resolver([[3, 1], [1, 2]], [1, 1])
    assert r["solucion"] == ["x1 = 1/5", "x2 = 2/5"]


def test_fracciones_como_texto():
    r = lineal.resolver([["1/2", 1], [1, 1]], [2, 3])
    assert r["tipo"] == "unica" and r["solucion"] == ["x1 = 2", "x2 = 1"]


def test_pivote_cero_requiere_intercambio():
    r = lineal.resolver([[0, 1], [1, 1]], [2, 3])
    assert r["solucion"] == ["x1 = 1", "x2 = 2"]
    assert any("Intercambiar" in p for p in r["pasos"])


def test_infinitas():
    r = lineal.resolver([[1, 2], [2, 4]], [3, 6])
    assert r["tipo"] == "infinitas"
    assert "x2 = libre" in r["solucion"] and "x1 = 3 + (-2)*x2" in r["solucion"]


def test_sin_solucion():
    r = lineal.resolver([[1, 2], [2, 4]], [3, 7])
    assert r["tipo"] == "sin_solucion" and r["solucion"] == []


def test_mas_incognitas_que_ecuaciones():
    r = lineal.resolver([[1, 1, 1]], [3])
    assert r["tipo"] == "infinitas"


def test_mas_ecuaciones_que_incognitas_compatible():
    r = lineal.resolver([[1, 0], [0, 1], [1, 1]], [1, 2, 3])
    assert r["tipo"] == "unica" and r["solucion"] == ["x1 = 1", "x2 = 2"]


def test_mas_ecuaciones_que_incognitas_incompatible():
    assert lineal.resolver([[1, 0], [0, 1], [1, 1]], [1, 2, 4])["tipo"] == "sin_solucion"


@pytest.mark.parametrize("A,b", [([], []), ([[1, 2], [3]], [1, 2]), ([[1, 2]], [1, 2]), ([[1, "abc"]], [1])])
def test_entradas_invalidas(A, b):
    with pytest.raises(ValueError):
        lineal.resolver(A, b)


# ---------------- Jacobi / Gauss-Seidel ----------------
A = [[4, 1, 1], [1, 5, 2], [1, 2, 6]]
B = [6, 8, 9]


@pytest.mark.parametrize("metodo", ["jacobi", "gauss_seidel"])
def test_iterativo_converge_a_la_solucion_exacta(metodo):
    r = iter_.resolver(A, B, metodo, tolerancia=1e-10)
    exacta = lineal.resolver(A, B)["solucion"]  # [x1 = 1, x2 = 1, x3 = 1]
    assert r["convergio"] and r["diagonal_dominante"]
    for linea, esperado in zip(r["solucion"], exacta):
        assert float(linea.split("=")[1]) == pytest.approx(float(esperado.split("=")[1]), abs=1e-6)


def test_gauss_seidel_mas_rapido_que_jacobi():
    gs = iter_.resolver(A, B, "gauss_seidel", tolerancia=1e-8)["iteraciones"]
    ja = iter_.resolver(A, B, "jacobi", tolerancia=1e-8)["iteraciones"]
    assert gs < ja


def test_no_converge_si_no_es_dominante():
    r = iter_.resolver([[1, 3], [4, 1]], [4, 5], "jacobi", max_iter=50)
    assert not r["convergio"] and not r["diagonal_dominante"]


def test_cero_en_la_diagonal():
    with pytest.raises(ValueError, match="reordene"):
        iter_.resolver([[0, 1], [1, 1]], [1, 2])


def test_metodo_invalido():
    with pytest.raises(ValueError):
        iter_.resolver(A, B, "newton")


def test_matriz_no_cuadrada():
    with pytest.raises(ValueError):
        iter_.resolver([[1, 2, 3], [4, 5, 6]], [1, 2])


# ---------------- Regla de Cramer ----------------
def test_cramer_2x2():
    r = cramer.resolver([[1, 1], [1, -1]], [3, 1])
    assert r["tipo"] == "unica" and r["determinante"] == "-2"
    assert r["solucion"] == ["x1 = 2", "x2 = 1"]


def test_cramer_3x3():
    r = cramer.resolver([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])
    assert r["determinante"] == "-1" and r["solucion"] == ["x1 = 2", "x2 = 3", "x3 = -1"]
    assert r["determinantes_variables"] == {"det(A1)": "-2", "det(A2)": "-3", "det(A3)": "1"}


def test_cramer_fracciones():
    assert cramer.resolver([[3, 1], [1, 2]], [1, 1])["solucion"] == ["x1 = 1/5", "x2 = 2/5"]


def test_cramer_determinante_cero():
    r = cramer.resolver([[1, 2], [2, 4]], [3, 6])
    assert r["tipo"] == "no_aplicable" and r["solucion"] == [] and "resolver-sistema-lineal" in r["explicacion"]


def test_determinante_con_intercambio_de_filas():
    assert cramer.determinante([[0, 1], [1, 0]]) == -1


@pytest.mark.parametrize("A,b", [([[1, 2, 3], [4, 5, 6]], [1, 2]), ([[1, 2], [3, 4]], [1]), ([], [])])
def test_cramer_entradas_invalidas(A, b):
    with pytest.raises(ValueError):
        cramer.resolver(A, b)


# ---------------- Matriz inversa ----------------
def test_inversa_2x2():
    r = inversa.resolver([[2, 1], [5, 3]])
    assert r["invertible"] and r["inversa"] == [["3", "-1"], ["-5", "2"]] and r["determinante"] == "1"


def test_inversa_por_A_da_identidad():
    from fractions import Fraction
    A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    inv = [[Fraction(v) for v in f] for f in inversa.resolver(A)["inversa"]]
    for i in range(3):
        for j in range(3):
            assert sum(A[i][k] * inv[k][j] for k in range(3)) == (1 if i == j else 0)


def test_inversa_con_b_resuelve_el_sistema():
    r = inversa.resolver([[2, 1], [5, 3]], [1, 2])
    assert r["solucion"] == ["x1 = 1", "x2 = -1"]


def test_inversa_singular():
    r = inversa.resolver([[1, 2], [2, 4]])
    assert r["invertible"] is False and r["inversa"] == []


def test_inversa_necesita_intercambio():
    r = inversa.resolver([[0, 1], [1, 0]])
    assert r["invertible"] and r["inversa"] == [["0", "1"], ["1", "0"]] and r["determinante"] == "-1"


def test_inversa_no_cuadrada():
    with pytest.raises(ValueError):
        inversa.resolver([[1, 2, 3], [4, 5, 6]])


# ---------------- Consistencia entre skills ----------------
@pytest.mark.parametrize("A,b", [
    ([[2, 1], [5, 3]], [1, 2]),
    ([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]),
    ([[0, 2, 1], [1, 1, 1], [2, 1, 0]], [4, 6, 5]),
    ([["1/2", "1/3"], [1, 1]], [2, 3]),
    ([[4, -2, 1, 0], [1, 3, 0, 2], [0, 1, 5, -1], [2, 0, 1, 6]], [1, 2, 3, 4]),
])
def test_las_tres_skills_exactas_coinciden(A, b):
    g = lineal.resolver(A, b)["solucion"]
    assert cramer.resolver(A, b)["solucion"] == g
    assert inversa.resolver(A, b)["solucion"] == g
