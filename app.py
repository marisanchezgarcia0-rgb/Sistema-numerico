"""Lanzador de Streamlit desde la raíz del repositorio.

Permite ejecutar directamente:
    python -m streamlit run app.py
desde la carpeta Sistema-numerico.
"""
from pathlib import Path
import runpy
import sys

RAIZ_SISTEMA = Path(__file__).resolve().parent / "ecuaciones-skills" / "sistema"
sys.path.insert(0, str(RAIZ_SISTEMA))

# Ejecutar la aplicación principal
runpy.run_path(str(RAIZ_SISTEMA / "interfaz" / "app.py"), run_name="__main__")

