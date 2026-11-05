@echo off
title Tutor de Sistemas de Ecuaciones
echo Iniciando interfaz grafica de Streamlit...
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python -m streamlit run app.py
pause

