# Interfaz Gráfica Moderna con Streamlit & Visión IA

Aplicación web interactiva para resolver sistemas de ecuaciones lineales y métodos numéricos, con soporte para fotos de ejercicios manuscritos e impresos.

## Características

- 💬 **Tutor IA & Visión de Fotos:**
  - Chat interactivo con renderizado de fórmulas en LaTeX ($\LaTeX$).
  - Subida visual de fotos/imágenes de ejercicios (arrastrar y soltar archivo o foto directa con la cámara web).
  - Reconocimiento y transcripción de ecuaciones con Gemini Vision.
  - Explicación matemática paso a paso.
- 🧮 **Calculadora Directa:**
  - Sin necesidad de IA o internet.
  - Admite números enteros, decimales y fracciones exactas (`1/3`, `-5/2`).
  - Resolución paso a paso con Gauss-Jordan, Cramer, Inversa o Métodos Iterativos.
- 📊 **Comparador de Métodos:**
  - Resuelve el mismo sistema simultáneamente en los 4 métodos en paralelo.
- 🔑 **Diagnóstico en Vivo de la Clave Gemini:**
  - Verificación en tiempo real de conectividad, latencia y cuota.
  - Motor matemático local resiliente de respaldo (garantiza que la app nunca falle si la API de Gemini tiene demoras o alta demanda).

## Cómo ejecutar

Desde la carpeta `sistema/`:

```powershell
python -m streamlit run interfaz/app.py
```
