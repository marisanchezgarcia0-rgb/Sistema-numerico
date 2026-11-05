"""Interfaz de Usuario Moderna para el Tutor de Sistemas de Ecuaciones.

Incluye:
- Chat moderno con soporte de LaTeX y explicación paso a paso.
- Subida visual de fotos/imágenes de ejercicios (archivo o cámara en vivo).
- Diagnóstico en tiempo real de la clave Gemini API.
- Calculadora directa interactiva con soporte de fracciones.
- Comparador multitécnica de métodos numéricos.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path
from typing import Any

import streamlit as st
from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from agente import herramientas as h
from agente.agente import (
    diagnosticar_gemini,
    obtener_api_key,
    responder_sync,
    sincronizar_archivos_env,
)
from agente.parser_local import (
    detectar_skill_solicitada,
    extraer_sistema_completo,
    formatear_respuesta_local,
    matriz_a_latex,
    sistema_a_latex,
    vector_a_latex,
)
from agente.vision import procesar_imagen_con_gemini

# ------------------------------------------------------------------ Configuración de Página
st.set_page_config(
    page_title="Tutor de Sistemas de Ecuaciones & Visión IA",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sincronizar posibles archivos .ven.txt
sincronizar_archivos_env()

# ------------------------------------------------------------------ Estilos CSS Modernos
CSS_PERSONALIZADO = """
<style>
/* Tipografía y contenedor principal */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Banner de encabezado */
.header-container {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #0f766e 100%);
    border-radius: 16px;
    padding: 24px 30px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.header-title {
    font-size: 2.1rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 12px;
}
.header-subtitle {
    font-size: 0.98rem;
    opacity: 0.88;
    margin-top: 8px;
    line-height: 1.5;
}

/* Tarjetas de ejercicios y visión */
.card-vision {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 20px;
    backdrop-filter: blur(8px);
}

/* Badges estilizados */
.badge-skill {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
    background: rgba(99, 102, 241, 0.2);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.3);
    margin-right: 6px;
    margin-bottom: 4px;
}
.badge-status {
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
}
.status-green { background: #065f46; color: #34d399; }
.status-yellow { background: #78350f; color: #fbbf24; }
.status-red { background: #7f1d1d; color: #f87171; }

/* Botones rápidos de ejemplos */
.pill-button {
    border-radius: 20px !important;
    font-size: 0.85rem !important;
}

/* Caja de solución destacada */
.solucion-box {
    background: rgba(16, 185, 129, 0.08);
    border-left: 4px solid #10b981;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 12px 0;
}
</style>
"""
st.markdown(CSS_PERSONALIZADO, unsafe_allow_html=True)

# ------------------------------------------------------------------ Constantes
EJEMPLOS = [
    ("3x3 Gauss-Jordan", "Resuelve: 2x + y - z = 8; -3x - y + 2z = -11; -2x + y + 2z = -3"),
    ("Regla de Cramer", "Resuelve por Cramer: x + y = 3; x - y = 1"),
    ("Matriz Inversa", "Calcula la inversa de [[2,1],[5,3]]"),
    ("Gauss-Seidel", "Resuelve con Gauss-Seidel: 4x + y + z = 6; x + 5y + 2z = 8; x + 2y + 6z = 9"),
    ("Infinitas Soluciones", "Resuelve: x + y + z = 6; 2x + 2y + 2z = 12; x - y = 1"),
]

SKILLS_INFO = {
    "resolver-sistema-lineal": {
        "titulo": "Gauss-Jordan Exacto",
        "desc": "Aritmética exacta con fracciones. Determina solución única, infinitas o incompatible.",
        "icono": "⚡",
    },
    "regla-de-cramer": {
        "titulo": "Regla de Cramer",
        "desc": "Determinantes det(A) y det(Ai). Aplica a sistemas cuadrados con det(A) ≠ 0.",
        "icono": "📐",
    },
    "matriz-inversa": {
        "titulo": "Matriz Inversa [A | I]",
        "desc": "Inversión por operaciones elementales fila. Resuelve x = A⁻¹b si se da b.",
        "icono": "🔄",
    },
    "metodos-iterativos": {
        "titulo": "Métodos Iterativos",
        "desc": "Algoritmos de Jacobi y Gauss-Seidel con tabla de iteraciones y convergencia.",
        "icono": "📊",
    },
}

# ------------------------------------------------------------------ Funciones Auxiliares UI
def render_header():
    st.markdown(
        """
        <div class="header-container">
            <div class="header-title">
                <span>🧮</span>
                <span>Tutor Inteligente de Álgebra Lineal & Métodos Numéricos</span>
            </div>
            <div class="header-subtitle">
                Resolución exacta paso a paso con <b>Gauss-Jordan, Cramer, Matriz Inversa y Métodos Iterativos</b>. 
                Sube fotos de tus ejercicios o interactúa en lenguaje natural.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_resultado_skill(skill: str, res: dict[str, Any]) -> None:
    """Muestra el resultado exacto de una skill con formato visual y LaTeX."""
    if not res.get("ok"):
        st.error(f"❌ **Error en el cálculo:** {res.get('error', 'No se pudo calcular.')}")
        return

    st.success(res.get("explicacion", "Cálculo completado."))

    if res.get("solucion"):
        st.markdown("##### 🎯 Solución:")
        sol_items = res["solucion"]
        # Formatear solución en KaTeX
        st.code("\n".join(sol_items), language=None)

    if res.get("inversa"):
        st.markdown("##### 🔄 Matriz Inversa $A^{-1}$:")
        st.latex(matriz_a_latex(res["inversa"]))

    if res.get("determinantes_variables"):
        c1, c2 = st.columns(2)
        c1.metric(label="det(A)", value=str(res.get("determinante")))
        c2.json(res["determinantes_variables"])

    if res.get("tabla"):
        st.markdown("##### 📈 Tabla de Convergencia por Iteración:")
        datos_tabla = [
            {
                "Iteración": f["iter"],
                "Vector x": ", ".join(f"{v:.5f}" for v in f["x"]),
                "Error Relativo": f"{f['error']:.2e}",
            }
            for f in res["tabla"]
        ]
        st.dataframe(datos_tabla, use_container_width=True)

    pasos = res.get("pasos") or []
    if pasos:
        with st.expander(f"📋 Ver procedimiento paso a paso ({len(pasos)} pasos elementales)"):
            for i, p in enumerate(pasos, 1):
                st.markdown(f"**Paso {i}:** `{p}`")


def detalle_de_calculos(registros: list[dict[str, Any]]) -> None:
    """Muestra lo que calcularon los scripts matemáticos subyacentes."""
    with st.expander("🔍 Auditoría de Cálculos Exactos (Scripts de Python)"):
        for r in registros:
            nombre = r.get("skill", "skill")
            st.markdown(f"<span class='badge-skill'>{nombre}</span>", unsafe_allow_html=True)
            mostrar_resultado_skill(nombre, r.get("resultado", {}))


# ------------------------------------------------------------------ Barra Lateral
with st.sidebar:
    st.markdown("### ⚙️ Centro de Control")

    # Selector de Modo Principal
    st.markdown("#### 🧭 Modo de Operación")
    modo = st.radio(
        "Seleccione el modo:",
        ["💬 Tutor IA & Visión de Fotos", "🧮 Calculadora Directa", "📊 Comparador de Métodos"],
        label_visibility="collapsed",
    )

    st.divider()

    # Tarjetas de Skills Disponibles para el usuario
    st.markdown("#### 📚 Métodos Disponibles")
    for s_id, s_data in SKILLS_INFO.items():
        st.markdown(
            f"**{s_data['icono']} {s_data['titulo']}**  \n"
            f"<span style='font-size:0.82rem; opacity:0.8;'>{s_data['desc']}</span>",
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button("🗑️ Borrar Conversación", use_container_width=True):
        st.session_state["mensajes"] = []
        st.session_state["imagen_cargada"] = None
        st.rerun()

    st.divider()

    # ------------------------------------------------------------------ PANEL ADMINISTRADOR (PROTEGIDO)
    st.session_state.setdefault("admin_autenticado", False)

    if not st.session_state["admin_autenticado"]:
        with st.expander("🔒 Acceso Administrador", expanded=False):
            st.caption("Configuración interna de la API protegida para profesores o administradores.")
            clave_admin_input = st.text_input("Contraseña de Admin", type="password", key="admin_pwd_login")
            if st.button("🔓 Desbloquear Configuración", use_container_width=True):
                import os
                clave_esperada = os.environ.get("ADMIN_PASSWORD", "admin123")
                if clave_admin_input.strip() == clave_esperada:
                    st.session_state["admin_autenticado"] = True
                    st.toast("Acceso concedido como Administrador", icon="🔓")
                    st.rerun()
                else:
                    st.error("Contraseña de administrador incorrecta.")
        modo_preferido = True
    else:
        with st.expander("🛠️ Panel de Administrador (Activo)", expanded=True):
            st.success("✅ Sesión de Administrador iniciada")
            st.markdown("##### 🔑 Configuración de Gemini API")
            clave_actual = obtener_api_key() or ""
            nueva_clave = st.text_input(
                "Gemini API Key",
                value=clave_actual,
                type="password",
                placeholder="Pegue aquí su clave de Google AI Studio",
                help="Obtenga una clave gratuita en https://aistudio.google.com/apikey",
            )

            if nueva_clave and nueva_clave != clave_actual:
                import os
                os.environ["GEMINI_API_KEY"] = nueva_clave.strip()
                env_path = RAIZ / ".env"
                try:
                    env_path.write_text(f"GEMINI_API_KEY={nueva_clave.strip()}\n", encoding="utf-8")
                    st.toast("Clave guardada exitosamente en .env", icon="💾")
                except Exception:
                    pass

            if st.button("🧪 Probar Conexión con Gemini", use_container_width=True):
                with st.spinner("Probando conexión con Gemini..."):
                    diag = diagnosticar_gemini(nueva_clave.strip() if nueva_clave else None)
                    if diag.get("ok"):
                        st.success(f"✅ {diag['mensaje']}")
                    else:
                        st.warning(f"⚠️ {diag.get('mensaje')}")
                        if diag.get("recomendacion"):
                            st.caption(diag["recomendacion"])

            modo_preferido = st.toggle(
                "Priorizar IA Gemini sobre Motor Local",
                value=True,
                help="Si se desactiva o la API no responde, el sistema resuelve automáticamente con el motor matemático exacto.",
            )

            if st.button("🔒 Cerrar Sesión Administrador", use_container_width=True):
                st.session_state["admin_autenticado"] = False
                st.rerun()


# ==============================================================================
# MODO 1: TUTOR IA & VISIÓN DE FOTOS
# ==============================================================================
if modo == "💬 Tutor IA & Visión de Fotos":
    render_header()

    # ------------------------------------------------------------------ SECCIÓN DE VISIÓN (FOTOS/IMÁGENES)
    with st.expander("📸 **Subir Ejercicio por Imagen o Foto (Reconocimiento Inteligente)**", expanded=False):
        st.markdown(
            "Cargue una fotografía o captura de un ejercicio (escrito a mano o impreso). "
            "El sistema extraerá las ecuaciones con **Gemini Vision** y preparará la solución."
        )

        tab_archivo, tab_camara = st.tabs(["📁 Subir Archivo de Imagen", "📷 Tomar Foto con la Cámara"])
        imagen_para_procesar = None

        with tab_archivo:
            archivo_subido = st.file_uploader(
                "Seleccione una imagen del ejercicio",
                type=["png", "jpg", "jpeg", "webp"],
                help="Formatos aceptados: PNG, JPG, JPEG, WEBP",
            )
            if archivo_subido is not None:
                try:
                    imagen_para_procesar = Image.open(archivo_subido)
                except Exception as exc:
                    st.error(f"No se pudo cargar la imagen: {exc}")

        with tab_camara:
            foto_camara = st.camera_input("Enfoque su hoja o cuaderno y capture la foto:")
            if foto_camara is not None:
                try:
                    imagen_para_procesar = Image.open(foto_camara)
                except Exception as exc:
                    st.error(f"No se pudo capturar la imagen: {exc}")

        if imagen_para_procesar is not None:
            col_img, col_proc = st.columns([1, 1.2])

            with col_img:
                st.image(imagen_para_procesar, caption="Vista previa del ejercicio", use_container_width=True)

            with col_proc:
                st.markdown("##### 🔍 Análisis de la Imagen")
                instruccion_extra = st.text_input(
                    "Instrucción opcional (ej. 'Resolver por Cramer', 'Calcular inversa'):",
                    placeholder="Dejar en blanco para resolver automáticamente",
                )

                if st.button("✨ Analizar y Resolver Imagen con IA", type="primary", use_container_width=True):
                    with st.spinner("Analizando ecuaciones manuscritas o impresas con Visión IA..."):
                        res_vision = procesar_imagen_con_gemini(
                            imagen_para_procesar,
                            api_key=obtener_api_key(),
                            texto_usuario=instruccion_extra,
                        )

                    if res_vision.get("ok") and res_vision.get("encontrado"):
                        st.success(f"✅ **Ecuaciones detectadas:** {res_vision.get('descripcion')}")
                        st.latex(res_vision.get("transcripcion_latex", ""))

                        A_ext = res_vision.get("A")
                        b_ext = res_vision.get("b")
                        skill_sug = res_vision.get("metodo_sugerido", "resolver-sistema-lineal")

                        if A_ext:
                            # Resolver de inmediato con la skill correspondiente
                            h.RESULTADOS.clear()
                            res_calc = h.calcular(skill_sug, A_ext, b_ext)
                            detalles = list(h.RESULTADOS)
                            vars_ext = res_vision.get("variables") or [f"x{i+1}" for i in range(len(A_ext[0]))]

                            texto_final = formatear_respuesta_local(skill_sug, A_ext, b_ext, vars_ext, res_calc, {})

                            # Agregar al chat para que quede en el historial
                            st.session_state.setdefault("mensajes", []).append({
                                "role": "user",
                                "content": f"📷 [Imagen subida]: {res_vision.get('descripcion')}",
                                "imagen": imagen_para_procesar,
                            })
                            st.session_state["mensajes"].append({
                                "role": "assistant",
                                "content": texto_final,
                                "detalles": detalles,
                            })
                            st.rerun()
                        else:
                            st.warning("Se reconoció la imagen pero no se pudo estructurar la matriz. Intente escribirla manualmente.")
                    else:
                        st.error(res_vision.get("error", "No se detectó un sistema legible en la foto."))
                        st.info("💡 Consejo: Asegúrese de que la foto tenga buena luz, enfoque nítido y las ecuaciones estén bien contrastadas.")

    # ------------------------------------------------------------------ CHIPS DE EJEMPLOS RÁPIDOS
    st.markdown("##### ⚡ Ejemplos Rápidos de Prueba:")
    cols_ej = st.columns(len(EJEMPLOS))
    for idx, (label_ej, prompt_ej) in enumerate(EJEMPLOS):
        if cols_ej[idx].button(label_ej, key=f"ej_{idx}", use_container_width=True):
            st.session_state["mensaje_pendiente"] = prompt_ej

    st.divider()

    # ------------------------------------------------------------------ HISTORIAL DE MENSAJES (VENTANA DE CHAT)
    st.session_state.setdefault("mensajes", [])

    if not st.session_state["mensajes"]:
        st.info("👋 Escriba su sistema de ecuaciones en el campo inferior o elija uno de los ejemplos rápidos arriba.")

    for m in st.session_state["mensajes"]:
        with st.chat_message(m["role"]):
            if m.get("imagen"):
                st.image(m["imagen"], width=300)
            st.markdown(m["content"])
            if m.get("detalles"):
                detalle_de_calculos(m["detalles"])

    # ------------------------------------------------------------------ ENTRADA DEL CHAT
    entrada_usuario = st.chat_input("Escriba su sistema de ecuaciones o pregunta matemática...")
    prompt_a_procesar = entrada_usuario or st.session_state.pop("mensaje_pendiente", None)

    if prompt_a_procesar:
        historial_previo = [{"role": m["role"], "content": m["content"]} for m in st.session_state["mensajes"]]
        st.session_state["mensajes"].append({"role": "user", "content": prompt_a_procesar})

        with st.chat_message("user"):
            st.markdown(prompt_a_procesar)

        with st.chat_message("assistant"):
            with st.spinner("Procesando y resolviendo cálculo exacto..."):
                respuesta_texto, detalles_calc = responder_sync(
                    prompt_a_procesar,
                    historial=historial_previo,
                    api_key=obtener_api_key(),
                    preferir_ia=modo_preferido,
                )

            st.markdown(respuesta_texto)
            if detalles_calc:
                detalle_de_calculos(detalles_calc)

            st.session_state["mensajes"].append({
                "role": "assistant",
                "content": respuesta_texto,
                "detalles": detalles_calc,
            })


# ==============================================================================
# MODO 2: CALCULADORA DIRECTA (INTERACTIVA & SIN IA)
# ==============================================================================
elif modo == "🧮 Calculadora Directa":
    render_header()
    st.markdown("### 🧮 Calculadora Directa de Álgebra Lineal")
    st.caption("Cálculo matemático directo y determinista. Admite números enteros, decimales y fracciones exactas (ej. `1/3`, `-5/2`).")

    col_skill, col_dim = st.columns([2, 1])
    with col_skill:
        skill_seleccionada = st.selectbox(
            "Método de resolución",
            list(SKILLS_INFO.keys()),
            format_func=lambda s: f"{SKILLS_INFO[s]['icono']} {SKILLS_INFO[s]['titulo']}",
        )
    with col_dim:
        tamano = st.selectbox("Dimensiones predefinidas", ["3x3", "2x2", "4x4", "Personalizado"], index=0)

    # Valores por defecto según dimensión
    valores_defecto_A = {
        "2x2": "2 1\n1 -1",
        "3x3": "2 1 -1\n-3 -1 2\n-2 1 2",
        "4x4": "1 2 0 1\n0 1 1 0\n2 0 1 1\n1 1 0 2",
        "Personalizado": "2 1 -1\n-3 -1 2\n-2 1 2",
    }[tamano]

    valores_defecto_b = {
        "2x2": "3 1",
        "3x3": "8 -11 -3",
        "4x4": "4 2 5 3",
        "Personalizado": "8 -11 -3",
    }[tamano]

    col_A, col_b = st.columns([2, 1])
    with col_A:
        texto_A = st.text_area("Matriz de Coeficientes A (una fila por línea, valores separados por espacio)", valores_defecto_A, height=140)
    with col_b:
        texto_b = st.text_input("Vector b (términos independientes)", valores_defecto_b)
        if skill_seleccionada == "matriz-inversa":
            st.caption("ℹ️ En matriz inversa, si deja b vacío solo se calculará $A^{-1}$.")

    opciones_extra: dict[str, Any] = {}
    if skill_seleccionada == "metodos-iterativos":
        c_m1, c_m2, c_m3 = st.columns(3)
        opciones_extra["metodo"] = c_m1.selectbox("Algoritmo", ["gauss_seidel", "jacobi"], format_func=lambda x: "Gauss-Seidel" if x == "gauss_seidel" else "Jacobi")
        opciones_extra["tolerancia"] = c_m2.number_input("Tolerancia (error máx)", value=1e-6, format="%.1e")
        opciones_extra["max_iter"] = c_m3.number_input("Máximo de iteraciones", value=100, min_value=1, step=10)

    if st.button("🚀 Calcular con Resolución Paso a Paso", type="primary", use_container_width=True):
        try:
            mat_A = h.parsear_matriz(texto_A)
            vec_b = h.parsear_vector(texto_b) if (texto_b.strip() or skill_seleccionada != "matriz-inversa") else None
            h.RESULTADOS.clear()
            resultado = h.calcular(skill_seleccionada, mat_A, vec_b, **opciones_extra)
            mostrar_resultado_skill(skill_seleccionada, resultado)
        except Exception as exc:
            st.error(f"❌ Error al procesar los datos: {exc}")


# ==============================================================================
# MODO 3: COMPARADOR DE MÉTODOS
# ==============================================================================
elif modo == "📊 Comparador de Métodos":
    render_header()
    st.markdown("### 📊 Comparador Multitécnica de Métodos Numéricos")
    st.caption("Resuelva el mismo sistema simultáneamente con Gauss-Jordan, Cramer, Matriz Inversa y Métodos Iterativos para contrastar exactitud y convergencia.")

    c_cA, c_cb = st.columns([2, 1])
    mat_str = c_cA.text_area("Matriz A (cuadrada)", "4 1 1\n1 5 2\n1 2 6", height=120)
    vec_str = c_cb.text_input("Vector b", "6 8 9")

    if st.button("⚡ Comparar los 4 Métodos en Paralelo", type="primary", use_container_width=True):
        try:
            A_comp = h.parsear_matriz(mat_str)
            b_comp = h.parsear_vector(vec_str)

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                st.markdown("#### 1. Gauss-Jordan")
                res_gj = h.calcular("resolver-sistema-lineal", A_comp, b_comp)
                if res_gj.get("ok"):
                    st.code("\n".join(res_gj.get("solucion", [])))
                else:
                    st.error(res_gj.get("error"))

            with col2:
                st.markdown("#### 2. Regla de Cramer")
                res_cr = h.calcular("regla-de-cramer", A_comp, b_comp)
                if res_cr.get("ok"):
                    st.markdown(f"**det(A):** {res_cr.get('determinante')}")
                    st.code("\n".join(res_cr.get("solucion", [])))
                else:
                    st.error(res_cr.get("error"))

            with col3:
                st.markdown("#### 3. Matriz Inversa ($x = A^{-1}b$)")
                res_inv = h.calcular("matriz-inversa", A_comp, b_comp)
                if res_inv.get("ok"):
                    st.code("\n".join(res_inv.get("solucion", [])))
                else:
                    st.error(res_inv.get("error"))

            with col4:
                st.markdown("#### 4. Gauss-Seidel (Iterativo)")
                res_it = h.calcular("metodos-iterativos", A_comp, b_comp, metodo="gauss_seidel")
                if res_it.get("ok"):
                    st.markdown(f"**Iteraciones:** {res_it.get('iteraciones')}")
                    sol_approx = [f"x{i+1} ≈ {val:.5f}" for i, val in enumerate(res_it.get("solucion", []))]
                    st.code("\n".join(sol_approx))
                else:
                    st.error(res_it.get("error"))

        except Exception as exc:
            st.error(f"Error en los datos de entrada: {exc}")
