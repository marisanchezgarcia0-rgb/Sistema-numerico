# Fase 3 — Análisis y selección de tecnologías

Criterio de decisión: **entregar skills funcionales y probadas en 2 semanas**, con un equipo de poca experiencia. Se elige lo mínimo necesario y se deja anotado qué entra después.

## 3.1 Lenguaje

**Python 3.12.** Es el lenguaje obligatorio, tiene sintaxis clara y su biblioteca estándar ya trae lo necesario para este proyecto.

## 3.2 Backend (cálculo)

En este proyecto el "backend" son los **scripts de las skills**. No hay servidor.

| Herramienta | Uso | Por qué |
|-------------|-----|---------|
| `fractions.Fraction` (estándar) | Gauss-Jordan, determinantes (Cramer) e inversa exactos | Resultados como 4/5 en lugar de 0.8000000001 |
| `json` (estándar) | Entrada y salida de los scripts | Formato simple que la IA entiende y genera bien |
| `sys` / `argparse` (estándar) | Ejecutar el script desde la línea de comandos | La IA lo ejecuta con un solo comando |
| `float` (estándar) | Métodos iterativos | Aproximaciones con tolerancia |

**Ventaja:** los scripts no necesitan instalar ningún paquete. Funcionan en cualquier computador con Python.

## 3.3 El agente de IA (quien lee la skill)

| Opción | Cómo funciona | Pros | Contras | Decisión |
|--------|---------------|------|---------|----------|
| **Claude con skills** (claude.ai o Claude Code) | La IA carga la skill, lee el `SKILL.md` y ejecuta los scripts | Es el uso natural de las skills; no hay que programar el agente | Requiere una cuenta o plan que permita skills y ejecución de código | **Elegido** |
| Claude por API (Agent SDK) | Un programa propio entrega la skill al modelo y ejecuta los scripts | Control total y se puede integrar en una aplicación | Requiere API key y más programación | **Etapa 2** |
| Pegar el `SKILL.md` en el chat | El usuario copia las instrucciones y ejecuta el script él mismo | Funciona en cualquier chat | Menos automático | **Plan alterno** |

**Decisión que hay que validar el día 1:** confirmar con qué producto y qué plan el equipo puede usar skills. No se debe asumir; se prueba subiendo la skill `resolver-sistema-lineal` y comprobando que la IA la use.

## 3.4 Frontend (interfaz)

En el MVP, **la interfaz es la conversación con la IA**: el usuario escribe el sistema y la instrucción de usar la skill.

| Opción | Pros | Contras | Decisión |
|--------|------|---------|----------|
| **Chat con la IA** | Sin programar interfaz | Depende del producto de IA | **MVP** |
| **Streamlit** | Interfaz en Python puro, en horas; sirve como demo sin IA | Menos diseño | **Opcional (días 8–9)** |
| React + Vite | Muy personalizable | Requiere JavaScript/TypeScript | **Etapa 2** |

## 3.5 Pruebas y calidad

| Herramienta | Propósito |
|-------------|-----------|
| **pytest** | Pruebas automáticas de los scripts |
| **Batería de 24 sistemas** | Evaluar que la IA elige y usa bien cada skill (se registra en una tabla) |
| Git + GitHub | Control de versiones y trabajo en equipo |
| VS Code | Editor |

## 3.6 Tecnologías de la Etapa 2

| Mejora | Tecnología |
|--------|-----------|
| Sistemas no lineales | SymPy (derivadas y parseo seguro) |
| Aplicación propia con IA | SDK de Anthropic + FastAPI |
| Historial | SQLite |
| Frontend avanzado | React |
| Despliegue | Docker y GitHub Actions |

## 3.7 Resumen del stack del MVP

```
Lenguaje  : Python 3.12 (solo biblioteca estándar)
Skills    : 4 carpetas con SKILL.md + scripts/
Agente    : Claude con skills (plan alterno: pegar el SKILL.md)
Interfaz  : el chat con la IA (opcional: Streamlit)
Pruebas   : pytest + batería de 24 sistemas
Equipo    : Git, GitHub, VS Code
```

## 3.8 Ruta de aprendizaje

| Tema | Para qué | Cuándo |
|------|----------|--------|
| Listas, funciones, ciclos y condicionales | Escribir los scripts | Día 1–2 |
| `Fraction` y listas de listas | Gauss-Jordan | Día 2–3 |
| Determinantes y matriz inversa (concepto) | Skills 3 y 4 | Día 6 |
| JSON y lectura de archivos | Entrada y salida | Día 2 |
| pytest básico | Pruebas | Día 3 |
| Qué es un `SKILL.md` y cómo se redacta una buena descripción | Skills | Día 1 y 4 |
| Git básico | Trabajo en equipo | Día 1 en adelante |

## 3.9 Decisiones a validar con el equipo

1. ¿Con qué cuenta o producto de IA se usarán las skills? (verificar el día 1.)
2. ¿Quién se encarga de cada skill? (se recomiendan parejas.)
3. ¿Cómo se hará la demo final: con la IA en vivo o con capturas de respaldo?
