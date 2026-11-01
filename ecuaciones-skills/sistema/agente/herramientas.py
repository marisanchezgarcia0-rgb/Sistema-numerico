"""Herramientas que el agente puede llamar. Cada una envuelve un script de skills/.

Por seguridad el agente NO tiene acceso a la terminal: solo puede llamar a estas
cuatro funciones, que reciben datos y devuelven el resultado calculado por el script.

Los numeros se reciben como texto ("2", "-1.5", "1/3") para no perder exactitud con fracciones.
"""
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def _cargar(ruta: str, nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_lineal = _cargar("skills/resolver-sistema-lineal/scripts/resolver_lineal.py", "skill_lineal")
_iterativos = _cargar("skills/metodos-iterativos/scripts/iterativos.py", "skill_iterativos")
_cramer = _cargar("skills/regla-de-cramer/scripts/cramer.py", "skill_cramer")
_inversa = _cargar("skills/matriz-inversa/scripts/inversa.py", "skill_inversa")

# Resultados crudos de la ultima consulta (la interfaz los muestra como "detalle del calculo").
RESULTADOS: list[dict] = []


def _a_float(v) -> float:
    try:
        return float(Fraction(str(v).strip()))
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"Numero no valido: {v!r}")


def calcular(skill: str, A, b=None, **opciones) -> dict:
    """Ejecuta una skill por su nombre y devuelve el diccionario de resultado. Nunca lanza errores."""
    try:
        if skill == "resolver-sistema-lineal":
            salida = _lineal.resolver(A, b)
        elif skill == "regla-de-cramer":
            salida = _cramer.resolver(A, b)
        elif skill == "matriz-inversa":
            salida = _inversa.resolver(A, b if b else None)
        elif skill == "metodos-iterativos":
            x0 = opciones.get("x0")
            salida = _iterativos.resolver(
                [[_a_float(v) for v in fila] for fila in A],
                [_a_float(v) for v in b],
                opciones.get("metodo", "gauss_seidel"),
                [_a_float(v) for v in x0] if x0 else None,
                float(opciones.get("tolerancia", 1e-6)),
                int(opciones.get("max_iter", 100)),
            )
        else:
            raise ValueError(f"Skill desconocida: {skill}")
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        salida = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    RESULTADOS.append({"skill": skill, "resultado": salida})
    return salida


def _como_texto(salida: dict) -> str:
    return json.dumps(salida, ensure_ascii=False)


# ----------------------------------------------------------------------------
# Funciones que ve el agente (el nombre, los tipos y el docstring son su "manual")
# ----------------------------------------------------------------------------
def resolver_lineal(A: list[list[str]], b: list[str]) -> str:
    """Resuelve un sistema de ecuaciones lineales Ax = b por Gauss-Jordan con fracciones exactas.

    Clasifica el sistema: 'unica' (una solucion), 'infinitas' (variables libres) o 'sin_solucion'.
    A: matriz de coeficientes, una fila por ecuacion y una columna por variable (x1, x2, ...).
    b: terminos independientes, uno por ecuacion.
    Cada numero va como texto: "2", "-1.5" o "1/3". Si una variable no aparece, su coeficiente es "0".
    Devuelve JSON con 'tipo', 'solucion', 'pasos' y 'explicacion'.
    """
    return _como_texto(calcular("resolver-sistema-lineal", A, b))


def resolver_iterativo(
    A: list[list[str]],
    b: list[str],
    metodo: str = "gauss_seidel",
    x0: list[str] | None = None,
    tolerancia: float = 1e-6,
    max_iter: int = 100,
) -> str:
    """Resuelve Ax = b de forma aproximada con Jacobi o Gauss-Seidel y devuelve la tabla de iteraciones.

    A debe ser cuadrada. metodo: 'jacobi' o 'gauss_seidel'. x0: vector inicial (por defecto ceros).
    Cada numero va como texto: "4", "-1.5" o "1/3".
    Devuelve JSON con 'convergio', 'iteraciones', 'solucion', 'tabla' y 'diagonal_dominante'.
    """
    return _como_texto(calcular("metodos-iterativos", A, b, metodo=metodo, x0=x0,
                                tolerancia=tolerancia, max_iter=max_iter))


def resolver_cramer(A: list[list[str]], b: list[str]) -> str:
    """Resuelve un sistema lineal cuadrado Ax = b con la regla de Cramer.

    Devuelve JSON con det(A), el determinante de cada matriz modificada y la solucion exacta.
    Si det(A) = 0 devuelve tipo 'no_aplicable'. Cada numero va como texto: "2", "-1.5" o "1/3".
    """
    return _como_texto(calcular("regla-de-cramer", A, b))


def calcular_inversa(A: list[list[str]], b: list[str] | None = None) -> str:
    """Calcula la matriz inversa de A (cuadrada) por Gauss-Jordan y dice si es invertible.

    Si se da b, tambien resuelve Ax = b con x = A^-1 b. Cada numero va como texto: "2", "-1.5" o "1/3".
    Devuelve JSON con 'invertible', 'determinante', 'inversa', 'solucion' y 'pasos'.
    """
    return _como_texto(calcular("matriz-inversa", A, b))


HERRAMIENTAS = [resolver_lineal, resolver_iterativo, resolver_cramer, calcular_inversa]


# ----------------------------------------------------------------------------
# Ayudas para la "calculadora directa" de la interfaz (texto -> listas)
# ----------------------------------------------------------------------------
def parsear_matriz(texto: str) -> list[list[str]]:
    """Convierte texto como '2 1 -1' (una fila por linea, separado por espacios o comas) en una matriz."""
    filas = [[t for t in linea.replace(",", " ").split()] for linea in texto.strip().splitlines() if linea.strip()]
    if not filas:
        raise ValueError("Escriba al menos una fila de la matriz")
    return filas


def parsear_vector(texto: str) -> list[str]:
    """Convierte '8 -11 -3' (o con comas) en una lista de numeros como texto."""
    return [t for t in texto.replace(",", " ").split()]
