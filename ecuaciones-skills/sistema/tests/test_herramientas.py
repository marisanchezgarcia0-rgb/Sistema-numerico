"""Pruebas de las herramientas del agente (no requieren el SDK ni Streamlit)."""
import json

import pytest

from agente import herramientas as h


@pytest.fixture(autouse=True)
def limpiar():
    h.RESULTADOS.clear()


def test_resolver_lineal_devuelve_json_con_solucion():
    r = json.loads(h.resolver_lineal([["2", "1", "-1"], ["-3", "-1", "2"], ["-2", "1", "2"]], ["8", "-11", "-3"]))
    assert r["tipo"] == "unica" and r["solucion"] == ["x1 = 2", "x2 = 3", "x3 = -1"]


def test_acepta_numeros_enteros_aunque_se_pidan_como_texto():
    r = json.loads(h.resolver_lineal([[1, 1], [1, -1]], [3, 1]))
    assert r["solucion"] == ["x1 = 2", "x2 = 1"]


def test_fracciones_como_texto():
    r = json.loads(h.resolver_cramer([["1/2", "1/3"], ["1", "1"]], ["2", "3"]))
    assert r["solucion"] == ["x1 = 6", "x2 = -3"]


def test_inversa_con_b():
    r = json.loads(h.calcular_inversa([["2", "1"], ["5", "3"]], ["1", "2"]))
    assert r["invertible"] and r["solucion"] == ["x1 = 1", "x2 = -1"]


def test_inversa_sin_b():
    r = json.loads(h.calcular_inversa([["2", "1"], ["5", "3"]]))
    assert r["inversa"] == [["3", "-1"], ["-5", "2"]] and r["solucion"] == []


def test_iterativo_acepta_fracciones_y_converge():
    r = json.loads(h.resolver_iterativo([["4", "1", "1"], ["1", "5", "2"], ["1", "2", "6"]], ["6", "8", "9"]))
    assert r["convergio"] and r["diagonal_dominante"]


def test_errores_no_lanzan_excepcion():
    r = json.loads(h.resolver_lineal([["1", "2"], ["3"]], ["1", "2"]))
    assert r["ok"] is False and "error" in r


def test_numero_invalido_da_error_claro():
    r = json.loads(h.resolver_cramer([["a", "1"], ["1", "1"]], ["1", "2"]))
    assert r["ok"] is False and "no valido" in r["error"]


def test_skill_desconocida():
    assert h.calcular("inventada", [["1"]], ["1"])["ok"] is False


def test_registra_resultados_para_la_interfaz():
    h.resolver_cramer([["1", "1"], ["1", "-1"]], ["3", "1"])
    h.calcular_inversa([["2", "1"], ["5", "3"]])
    assert [r["skill"] for r in h.RESULTADOS] == ["regla-de-cramer", "matriz-inversa"]


def test_herramientas_tienen_docstring_y_nombre_unico():
    nombres = [f.__name__ for f in h.HERRAMIENTAS]
    assert len(nombres) == len(set(nombres)) == 4
    assert all(f.__doc__ and len(f.__doc__) > 40 for f in h.HERRAMIENTAS)


def test_parsear_matriz_y_vector():
    assert h.parsear_matriz("2 1 -1\n-3, -1, 2\n\n") == [["2", "1", "-1"], ["-3", "-1", "2"]]
    assert h.parsear_vector("8, -11  -3") == ["8", "-11", "-3"]


def test_parsear_matriz_vacia():
    with pytest.raises(ValueError):
        h.parsear_matriz("   \n ")


def test_el_agente_no_tiene_comandos_de_terminal():
    """El agente debe bloquear la terminal: la configuracion lo deniega por nombre."""
    import inspect
    from agente import agente

    codigo = inspect.getsource(agente.crear_config)
    assert 'deny("*")' in codigo and "read_only" in codigo and "run_command" not in codigo.replace('deny("*")', "")


def test_prompt_incluye_historial_y_mensaje():
    from agente import agente

    p = agente._armar_prompt("¿y por Cramer?", [{"role": "user", "content": "x+y=3"}, {"role": "assistant", "content": "ok"}])
    assert "Usuario: x+y=3" in p and "Asistente: ok" in p and p.rstrip().endswith("¿y por Cramer?")
