"""Agente para resolución de sistemas de ecuaciones.

Soporta dos motores de ejecución integrados:
1. Motor IA Gemini (vía google-genai o Antigravity SDK con tools).
2. Motor Matemático Local Resiliente (parser algebraico exacto con Fractions),
   que actúa como respaldo automático si la API de Gemini tiene problemas de
   conexión, demanda alta (503), clave faltante o cuota agotada.

Esto garantiza que el usuario NUNCA se quede sin respuesta.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any

from agente import herramientas as h
from agente.parser_local import (
    detectar_skill_solicitada,
    extraer_sistema_completo,
    formatear_respuesta_local,
)

RAIZ = Path(__file__).resolve().parents[1]
MAX_CARACTERES = 3000

INSTRUCCIONES_SISTEMA = (
    "Eres un tutor universitario de Álgebra Lineal y Métodos Numéricos. Responde siempre en español, con calidez y claridad pedagógica.\n"
    "Dispones de cuatro herramientas exactas: resolver_lineal, resolver_iterativo, resolver_cramer y calcular_inversa.\n"
    "REGLA CRÍTICA: NUNCA calcules los resultados aritméticos por ti mismo. Llama SIEMPRE a la herramienta correspondiente "
    "con las matrices y vectores parseados (usando cadenas numéricas como '2', '-1.5', '1/3').\n"
    "Explica los resultados usando notación matemática clara con LaTeX ($...$ para fórmulas en línea y $$...$$ para matrices y sistemas).\n"
    "Si un sistema no tiene solución o tiene infinitas, explica su significado geométrico.\n"
    "Si la consulta no está relacionada con sistemas de ecuaciones o álgebra lineal, responde cortésmente invitando a plantear un problema matemático."
)


def crear_config(api_key: str | None = None):
    """Configuracion del agente (Antigravity SDK): carga skills, solo 4 herramientas y NINGUN acceso a la terminal."""
    from google.antigravity import CapabilitiesConfig, LocalAgentConfig
    from google.antigravity.hooks.policy import allow, deny
    from google.antigravity.types import BuiltinTools

    clave = api_key or obtener_api_key()
    return LocalAgentConfig(
        api_key=clave,
        skills_paths=[str(RAIZ / "skills")],
        tools=h.HERRAMIENTAS,
        capabilities=CapabilitiesConfig(enabled_tools=BuiltinTools.read_only()),
        policies=[deny("*"), allow("view_file"), *[allow(f.__name__) for f in h.HERRAMIENTAS]],
    )


def _armar_prompt(mensaje: str, historial: list[dict] | None) -> str:
    """Construye el prompt con instrucciones, historial previo y mensaje actual."""
    partes = [INSTRUCCIONES_SISTEMA]
    if historial:
        previo = "\n".join(
            f"{'Usuario' if m['role'] == 'user' else 'Asistente'}: {m['content']}" for m in historial[-10:]
        )
        partes.append("Conversacion previa:\n" + previo)
    partes.append("Mensaje actual del usuario:\n" + mensaje)
    return "\n\n".join(partes)


def sincronizar_archivos_env() -> None:
    """Detecta archivos mal nombrados como .ven.txt o .env.txt y los sincroniza a .env."""
    candidatos_erroneos = [
        RAIZ / ".ven.txt",
        RAIZ / ".env.txt",
        RAIZ.parent / ".ven.txt",
        RAIZ.parent / ".env.txt",
    ]
    env_oficial = RAIZ / ".env"

    for cand in candidatos_erroneos:
        if cand.exists():
            contenido = cand.read_text(encoding="utf-8").strip()
            if "GEMINI_API_KEY=" in contenido and (not env_oficial.exists() or env_oficial.stat().st_size == 0):
                try:
                    env_oficial.write_text(contenido, encoding="utf-8")
                except Exception:
                    pass


def _cargar_clave() -> None:
    """Carga GEMINI_API_KEY desde .env, .ven.txt o carpetas superiores."""
    sincronizar_archivos_env()

    rutas_posibles = [
        RAIZ / ".env",
        RAIZ / ".ven.txt",
        RAIZ / ".env.txt",
        RAIZ.parent / ".env",
        RAIZ.parent / ".ven.txt",
    ]

    for ruta in rutas_posibles:
        if ruta.exists():
            try:
                for linea in ruta.read_text(encoding="utf-8").splitlines():
                    linea = linea.strip()
                    if linea and not linea.startswith("#") and "=" in linea:
                        nombre, valor = linea.split("=", 1)
                        nombre_limpio = nombre.strip()
                        valor_limpio = valor.strip().strip('"').strip("'")
                        if nombre_limpio == "GEMINI_API_KEY" and valor_limpio:
                            os.environ.setdefault("GEMINI_API_KEY", valor_limpio)
            except Exception:
                pass


def obtener_api_key() -> str | None:
    """Devuelve la clave activa de Gemini o None si no existe."""
    _cargar_clave()
    key = os.environ.get("GEMINI_API_KEY")
    return key.strip() if key else None


def diagnosticar_gemini(api_key: str | None = None) -> dict[str, Any]:
    """Prueba la conexión real con la API de Gemini y devuelve un diagnóstico completo."""
    clave = api_key or obtener_api_key()
    if not clave:
        return {
            "ok": False,
            "estado": "sin_clave",
            "mensaje": "No se encontró GEMINI_API_KEY en sistema/.env ni en el entorno.",
            "recomendacion": "Ingrese su clave en el campo de la barra lateral o cree el archivo sistema/.env.",
        }

    # Probar conexión real usando google-genai
    inicio = time.time()
    try:
        from google import genai
        client = genai.Client(api_key=clave, http_options={"timeout": 8})

        # Probar modelos recomendados
        modelos_a_probar = ["gemini-2.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]
        ultimo_err = None
        for mod in modelos_a_probar:
            try:
                resp = client.models.generate_content(
                    model=mod,
                    contents="Responde solo: OK",
                )
                latencia = round((time.time() - inicio) * 1000)
                return {
                    "ok": True,
                    "estado": "conectado",
                    "modelo": mod,
                    "latencia_ms": latencia,
                    "mensaje": f"Conexión exitosa con Gemini ({mod}) en {latencia} ms.",
                }
            except Exception as e:
                ultimo_err = e
                continue

        latencia = round((time.time() - inicio) * 1000)
        err_msg = str(ultimo_err)
        err_tipo = type(ultimo_err).__name__

        if "403" in err_msg or "API_KEY_INVALID" in err_msg or "Invalid API Key" in err_msg:
            return {
                "ok": False,
                "estado": "clave_invalida",
                "mensaje": "La clave ingresada no es válida o fue rechazada por Google AI Studio.",
                "recomendacion": "Obtenga una nueva clave gratuita en https://aistudio.google.com/apikey",
                "detalle": err_msg or err_tipo,
            }
        elif "503" in err_msg or "UNAVAILABLE" in err_msg or "high demand" in err_msg.lower():
            return {
                "ok": False,
                "estado": "alta_demanda",
                "mensaje": "Los servidores de Gemini tienen alta demanda en este momento (Error 503).",
                "recomendacion": "El sistema usará automáticamente el motor matemático exacto local.",
                "detalle": err_msg or err_tipo,
            }
        elif "timeout" in err_msg.lower() or "timeout" in err_tipo.lower():
            return {
                "ok": False,
                "estado": "timeout",
                "mensaje": "Tiempo de espera agotado al conectar con Google (ConnectTimeout).",
                "recomendacion": (
                    "No se pudo alcanzar generativelanguage.googleapis.com:443. "
                    "Esto suele ocurrir por restricción geográfica de red/ISP (se soluciona activando una VPN o Cloudflare WARP) "
                    "o por un firewall. ¡El motor matemático local sigue funcionando al 100% en el chat!"
                ),
                "detalle": err_tipo,
            }
        else:
            return {
                "ok": False,
                "estado": "error_api",
                "mensaje": f"Fallo al consultar la API: {err_tipo}",
                "detalle": err_msg or err_tipo,
            }

    except Exception as exc:
        return {
            "ok": False,
            "estado": "error_cliente",
            "mensaje": f"Error inicializando cliente: {type(exc).__name__}: {exc}",
        }


def resolver_con_motor_local(mensaje: str) -> tuple[str, list[dict]]:
    """Resuelve cualquier sistema usando el motor algebraico local sin requerir IA."""
    h.RESULTADOS.clear()
    A, b, variables = extraer_sistema_completo(mensaje)

    if not A:
        # No se detectó un sistema numérico explícito en el texto
        respuesta = (
            "👋 **¡Hola! Soy tu tutor de Sistemas de Ecuaciones y Métodos Numéricos.**\n\n"
            "Puedo ayudarte a resolver sistemas de ecuaciones lineales, calcular matrices inversas, "
            "aplicar la regla de Cramer o métodos iterativos como Jacobi y Gauss-Seidel.\n\n"
            "💡 **Ejemplos de cómo puedes escribirme:**\n"
            "- *Resuelve: 2x + y - z = 8; -3x - y + 2z = -11; -2x + y + 2z = -3*\n"
            "- *Resuelve por Cramer: x + y = 3; x - y = 1*\n"
            "- *Calcula la inversa de [[2,1],[5,3]]*\n"
            "- *Resuelve por Gauss-Seidel: 4x + y + z = 6; x + 5y + 2z = 8; x + 2y + 6z = 9*\n\n"
            "📸 También puedes **subir una foto o captura** de tu ejercicio usando el panel superior."
        )
        return respuesta, []

    skill, opciones = detectar_skill_solicitada(mensaje, A)
    res = h.calcular(skill, A, b, **opciones)
    vars_usadas = variables or [f"x{i+1}" for i in range(len(A[0]))]
    texto_formateado = formatear_respuesta_local(skill, A, b, vars_usadas, res, opciones)
    detalles = list(h.RESULTADOS)
    return texto_formateado, detalles


def responder_con_gemini_direct(
    mensaje: str,
    historial: list[dict] | None = None,
    api_key: str | None = None,
) -> tuple[str, list[dict]]:
    """Consulta directa a Gemini con ejecución de herramientas mediante Chat y timeout estricto."""
    clave = api_key or obtener_api_key()
    if not clave:
        raise RuntimeError("No hay clave de Gemini configurada.")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=clave, http_options={"timeout": 14})
    h.RESULTADOS.clear()

    modelos_candidatos = ["gemini-2.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]
    ultimo_error = None

    for modelo in modelos_candidatos:
        try:
            config = types.GenerateContentConfig(
                temperature=0.1,
                system_instruction=INSTRUCCIONES_SISTEMA,
                tools=h.HERRAMIENTAS,
            )

            # Usar sesion de chat con ejecucion automatica de funciones
            chat = client.chats.create(model=modelo, config=config)
            response = chat.send_message(mensaje)

            detalles = list(h.RESULTADOS)
            texto_respuesta = response.text or ""

            # Si el modelo calculo pero el texto es escueto, enriquecer con formato matematico
            if detalles and (len(texto_respuesta.strip()) < 50 or "{" in texto_respuesta):
                ultimo_det = detalles[-1]
                A, b, v = extraer_sistema_completo(mensaje)
                vars_usadas = v or [f"x{i+1}" for i in range(3)]
                texto_respuesta = formatear_respuesta_local(
                    ultimo_det["skill"], A or [], b, vars_usadas, ultimo_det["resultado"], {}
                )

            return texto_respuesta, detalles

        except Exception as exc:
            ultimo_error = exc
            continue

    raise RuntimeError(f"Fallo en comunicación con Gemini: {type(ultimo_error).__name__}: {ultimo_error}")


def responder_sync(
    mensaje: str,
    historial: list[dict] | None = None,
    api_key: str | None = None,
    preferir_ia: bool = True,
) -> tuple[str, list[dict]]:
    """Función principal consumida por la interfaz de Streamlit.
    
    1. Si se prefiere IA y hay clave: intenta Gemini con herramientas.
    2. Si Gemini falla (timeout, 503, cuota) o no hay clave: usa el Motor Matemático Local.
    """
    mensaje = mensaje.strip()[:MAX_CARACTERES]
    if not mensaje:
        return "Por favor ingrese un mensaje o sistema de ecuaciones.", []

    clave = api_key or obtener_api_key()

    # Intentar con IA si está habilitado y hay clave disponible
    if preferir_ia and clave:
        try:
            return responder_con_gemini_direct(mensaje, historial, clave)
        except Exception:
            # Transición transparente al motor local sin alertas intrusivas
            return resolver_con_motor_local(mensaje)

    # Modo sin IA o sin clave: motor local directo
    return resolver_con_motor_local(mensaje)


if __name__ == "__main__":
    print("Iniciando Agente de Sistemas Numéricos...")
    diag = diagnosticar_gemini()
    print("Diagnóstico de conexión:", diag)
    test_msg = "Resuelve: 2x + y - z = 8; -3x - y + 2z = -11; -2x + y + 2z = -3"
    texto, det = responder_sync(test_msg)
    print("\nRespuesta obtenida con éxito (longitud:", len(texto), "caracteres)")
