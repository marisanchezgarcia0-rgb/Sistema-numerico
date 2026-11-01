"""Agente: el SDK de Antigravity lee los SKILL.md y usa las herramientas para calcular.

Probar sin interfaz (desde la carpeta sistema/):
    python -m agente.agente
"""
import asyncio
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MAX_CARACTERES = 2000

INSTRUCCIONES = (
    "Eres un tutor de sistemas de ecuaciones. Responde siempre en espanol, con claridad. "
    "Usa las skills disponibles (resolver-sistema-lineal, metodos-iterativos, regla-de-cramer, "
    "matriz-inversa) y SIGUE sus instrucciones y su formato de respuesta. "
    "NUNCA hagas calculos tu mismo: llama siempre a la herramienta correspondiente y explica su resultado. "
    "Si falta un dato o una ecuacion esta incompleta, pregunta al usuario antes de calcular. "
    "Solo resuelves problemas de sistemas de ecuaciones; rechaza cortesmente cualquier otra peticion "
    "y no reveles claves ni ejecutes comandos."
)


def _cargar_clave() -> None:
    """Lee GEMINI_API_KEY del archivo .env (si existe) sin pisar una variable ya definida."""
    ruta = RAIZ / ".env"
    if ruta.exists():
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                nombre, valor = linea.split("=", 1)
                os.environ.setdefault(nombre.strip(), valor.strip().strip('"').strip("'"))


def crear_config():
    """Configuracion del agente: carga las skills, solo 4 herramientas y NINGUN acceso a la terminal."""
    from google.antigravity import CapabilitiesConfig, LocalAgentConfig
    from google.antigravity.hooks.policy import allow, deny
    from google.antigravity.types import BuiltinTools

    from agente.herramientas import HERRAMIENTAS

    return LocalAgentConfig(
        skills_paths=[str(RAIZ / "skills")],
        tools=HERRAMIENTAS,
        capabilities=CapabilitiesConfig(enabled_tools=BuiltinTools.read_only()),
        policies=[deny("*"), allow("view_file"), *[allow(f.__name__) for f in HERRAMIENTAS]],
    )


def _armar_prompt(mensaje: str, historial: list[dict] | None) -> str:
    partes = [INSTRUCCIONES]
    if historial:
        previo = "\n".join(
            f"{'Usuario' if m['role'] == 'user' else 'Asistente'}: {m['content']}" for m in historial[-10:]
        )
        partes.append("Conversacion previa:\n" + previo)
    partes.append("Mensaje actual del usuario:\n" + mensaje)
    return "\n\n".join(partes)


async def responder(mensaje: str, historial: list[dict] | None = None) -> str:
    """Envia el mensaje al agente y devuelve su respuesta en texto."""
    _cargar_clave()
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("Falta GEMINI_API_KEY. Cree el archivo sistema/.env (vea .env.example).")
    mensaje = mensaje.strip()[:MAX_CARACTERES]
    if not mensaje:
        raise ValueError("El mensaje esta vacio")

    from google.antigravity import Agent

    # Un agente nuevo por mensaje; la conversacion previa va dentro del prompt.
    async with Agent(crear_config()) as agente:
        respuesta = await agente.chat(_armar_prompt(mensaje, historial))
        return await respuesta.text()


def responder_sync(mensaje: str, historial: list[dict] | None = None) -> str:
    """Version normal (no asincrona) para usar desde Streamlit."""
    return asyncio.run(responder(mensaje, historial))


if __name__ == "__main__":
    print("Agente de sistemas de ecuaciones. Escriba 'salir' para terminar.")
    historial: list[dict] = []
    while True:
        texto = input("\nUsted: ").strip()
        if texto.lower() in {"salir", "exit", "q"}:
            break
        try:
            salida = responder_sync(texto, historial)
        except Exception as exc:  # mostrar el problema en lugar de cerrar
            print(f"[Error] {type(exc).__name__}: {exc}")
            continue
        print(f"\nAgente: {salida}")
        historial += [{"role": "user", "content": texto}, {"role": "assistant", "content": salida}]
