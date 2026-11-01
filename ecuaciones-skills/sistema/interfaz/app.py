"""Interfaz de usuario (Streamlit).

Ejecutar desde la carpeta sistema/:
    python -m streamlit run interfaz/app.py
"""
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from agente import herramientas as h  # noqa: E402

st.set_page_config(page_title="Resolutor de sistemas de ecuaciones", page_icon="🧮", layout="wide")

EJEMPLOS = [
    "Resuelve: 2x + y - z = 8; -3x - y + 2z = -11; -2x + y + 2z = -3",
    "Resuelve por Cramer: x + y = 3; x - y = 1",
    "Calcula la inversa de [[2,1],[5,3]]",
    "Resuelve con Gauss-Seidel: 4x + y + z = 6; x + 5y + 2z = 8; x + 2y + 6z = 9",
]
SKILLS = {
    "resolver-sistema-lineal": "Gauss-Jordan exacto. Dice si hay solucion unica, infinitas o ninguna.",
    "metodos-iterativos": "Jacobi y Gauss-Seidel con tabla de iteraciones.",
    "regla-de-cramer": "Determinantes de A y de cada matriz modificada.",
    "matriz-inversa": "Inversa de A y, si se da b, la solucion de Ax = b.",
}


# ------------------------------------------------------------------ mostrar resultados
def mostrar_resultado(skill: str, res: dict) -> None:
    """Muestra el resultado de una skill: errores, solucion, tablas y pasos."""
    if not res.get("ok"):
        st.error(res.get("error", "No se pudo calcular."))
        return
    st.success(res.get("explicacion", "Listo."))
    if res.get("solucion"):
        st.markdown("**Solucion**")
        st.code("\n".join(res["solucion"]), language=None)
    if res.get("inversa"):
        st.markdown("**Matriz inversa**")
        st.table(res["inversa"])
    if res.get("determinantes_variables"):
        st.markdown(f"**det(A)** = {res.get('determinante')}")
        st.json(res["determinantes_variables"])
    if res.get("tabla"):
        st.markdown("**Tabla de iteraciones**")
        st.dataframe(
            [{"iteracion": f["iter"], "x": ", ".join(str(v) for v in f["x"]), "error": f"{f['error']:.2e}"}
             for f in res["tabla"]],
        )
    pasos = (res.get("pasos") or [])
    if pasos:
        with st.expander(f"Ver los {len(pasos)} pasos"):
            for i, p in enumerate(pasos, 1):
                st.text(f"{i}. {p}")


def detalle_de_calculos(registros: list[dict]) -> None:
    """Muestra lo que calcularon realmente los scripts (para verificar al agente)."""
    with st.expander("Detalle del calculo (resultado exacto de los scripts)"):
        for r in registros:
            st.caption(f"Skill usada: {r['skill']}")
            mostrar_resultado(r["skill"], r["resultado"])


# ------------------------------------------------------------------ barra lateral
with st.sidebar:
    st.title("🧮 Sistemas de ecuaciones")
    modo = st.radio("Modo", ["Chat con el agente", "Calculadora directa"])
    st.markdown("**Skills disponibles**")
    for nombre, desc in SKILLS.items():
        st.markdown(f"- `{nombre}`: {desc}")
    if modo == "Chat con el agente":
        st.markdown("**Ejemplos**")
        for ej in EJEMPLOS:
            if st.button(ej, key=ej):
                st.session_state["pendiente"] = ej
        if st.button("Borrar conversacion"):
            st.session_state["mensajes"] = []
            st.rerun()

# ------------------------------------------------------------------ modo chat
if modo == "Chat con el agente":
    st.header("Chat con el agente")
    st.caption("Escriba su sistema de ecuaciones. El agente elige la skill y los scripts hacen el calculo exacto.")
    st.session_state.setdefault("mensajes", [])

    for m in st.session_state["mensajes"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m.get("detalles"):
                detalle_de_calculos(m["detalles"])

    entrada = st.chat_input("Escriba su sistema o su pregunta...") or st.session_state.pop("pendiente", None)
    if entrada:
        historial = [{"role": m["role"], "content": m["content"]} for m in st.session_state["mensajes"]]
        st.session_state["mensajes"].append({"role": "user", "content": entrada})
        with st.chat_message("user"):
            st.markdown(entrada)
        with st.chat_message("assistant"):
            h.RESULTADOS.clear()
            try:
                from agente.agente import responder_sync

                with st.spinner("Resolviendo..."):
                    respuesta = responder_sync(entrada, historial)
                detalles = list(h.RESULTADOS)
                st.markdown(respuesta)
                if detalles:
                    detalle_de_calculos(detalles)
                st.session_state["mensajes"].append(
                    {"role": "assistant", "content": respuesta, "detalles": detalles}
                )
            except RuntimeError as exc:  # por ejemplo, falta la clave
                st.error(str(exc))
            except ImportError:
                st.error("Falta instalar el SDK: ejecute  python -m pip install -r requirements.txt")
            except Exception as exc:  # cualquier otro fallo del agente
                st.error("El agente no pudo responder. Pruebe de nuevo o use la Calculadora directa.")
                with st.expander("Detalle tecnico"):
                    st.code(f"{type(exc).__name__}: {exc}")

# ------------------------------------------------------------------ modo calculadora directa
else:
    st.header("Calculadora directa (sin IA)")
    st.caption("Escriba la matriz con una fila por linea. Acepta enteros, decimales y fracciones como 1/3.")
    skill = st.selectbox("Skill", list(SKILLS), format_func=lambda s: f"{s}: {SKILLS[s]}")
    c1, c2 = st.columns(2)
    texto_a = c1.text_area("Matriz A (una fila por linea)", "2 1 -1\n-3 -1 2\n-2 1 2", height=160)
    texto_b = c2.text_input("Vector b (terminos independientes)", "8 -11 -3")
    opciones = {}
    if skill == "metodos-iterativos":
        o1, o2, o3 = st.columns(3)
        opciones["metodo"] = o1.selectbox("Metodo", ["gauss_seidel", "jacobi"])
        opciones["tolerancia"] = o2.number_input("Tolerancia", value=1e-6, format="%.1e")
        opciones["max_iter"] = o3.number_input("Maximo de iteraciones", value=100, min_value=1, step=10)
    if skill == "matriz-inversa":
        st.caption("Si deja b vacio, solo se calcula la inversa.")

    if st.button("Calcular", type="primary"):
        try:
            A = h.parsear_matriz(texto_a)
            b = h.parsear_vector(texto_b)
            res = h.calcular(skill, A, b, **opciones)
        except ValueError as exc:
            res = {"ok": False, "error": str(exc)}
        mostrar_resultado(skill, res)
