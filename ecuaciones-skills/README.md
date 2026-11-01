# Skills para resolver sistemas de ecuaciones

Conjunto de *skills* (carpetas con `SKILL.md` + scripts de Python) que una IA lee y ejecuta para resolver sistemas de ecuaciones siempre con el mismo método, el mismo formato y cálculo exacto. El usuario solo entrega el sistema y le dice a la IA que use la skill.

> La IA lee, interpreta y explica; el script de Python calcula.

## Estructura

```
ecuaciones-skills/
├── README.md
├── documentacion/            Todo lo escrito: planificación y cronograma
│   ├── Planificacion_Skills_Ecuaciones_Fases_1-4.docx
│   ├── fase-1-planteamiento.md
│   ├── fase-2-requerimientos.md
│   ├── fase-3-tecnologias.md
│   └── fase-4-arquitectura-cronograma.md
└── sistema/                  Todo lo que hace funcionar el sistema
    ├── skills/               Las 4 skills (SKILL.md + scripts/)
    ├── agente/               El agente (SDK de Antigravity) y sus herramientas
    ├── interfaz/             La aplicación para el usuario (Streamlit)
    ├── tests/                Pruebas automáticas (pytest)
    ├── ejemplos/             Entradas JSON de ejemplo
    ├── evaluacion/           Batería de 24 casos para evaluar a la IA
    ├── requirements.txt      Lo que hay que instalar
    └── .env.example          Plantilla para la clave de Gemini
```

## Skills incluidas (MVP: 4 skills)

| Skill | Qué hace |
|-------|----------|
| [`resolver-sistema-lineal`](sistema/skills/resolver-sistema-lineal/SKILL.md) | Gauss-Jordan con fracciones exactas; clasifica el sistema (única, infinitas o sin solución) |
| [`metodos-iterativos`](sistema/skills/metodos-iterativos/SKILL.md) | Jacobi y Gauss-Seidel con tabla de iteraciones y chequeo de convergencia |
| [`regla-de-cramer`](sistema/skills/regla-de-cramer/SKILL.md) | Regla de Cramer: det(A), det(Ai) y solución; avisa si det(A) = 0 |
| [`matriz-inversa`](sistema/skills/matriz-inversa/SKILL.md) | Inversa por Gauss-Jordan sobre [A \| I]; indica si es invertible y resuelve Ax = b |

## Probar los scripts (sin IA)

Desde la carpeta `sistema/`:

```bash
cd sistema
python skills/resolver-sistema-lineal/scripts/resolver_lineal.py ejemplos/lineal_3x3.json
python skills/metodos-iterativos/scripts/iterativos.py ejemplos/iterativo_3x3.json
python skills/regla-de-cramer/scripts/cramer.py ejemplos/cramer_3x3.json
python skills/matriz-inversa/scripts/inversa.py ejemplos/inversa_2x2.json
pip install pytest && pytest      # 55 pruebas
```

No hace falta instalar nada más: los scripts usan solo la biblioteca estándar de Python.

## Ejecutar la aplicación

Desde la carpeta `sistema/` (en PowerShell):

```powershell
# 1. Instalar lo necesario (una sola vez)
python -m pip install -r requirements.txt

# 2. Crear el archivo .env con su clave de Gemini (una sola vez)
Copy-Item .env.example .env
notepad .env        # reemplace "pegue_aqui_su_clave" por su clave y guarde

# 3. (Opcional) Probar el agente en la terminal, sin interfaz
python -m agente.agente

# 4. Abrir la aplicación
python -m streamlit run interfaz/app.py
```

La interfaz tiene dos modos:

- **Chat con el agente:** escribe el sistema en lenguaje natural; el agente elige la skill y los scripts calculan. Cada respuesta incluye el "detalle del cálculo" exacto de los scripts, para verificar al agente.
- **Calculadora directa:** funciona **sin IA y sin clave**. Sirve para demostrar las skills aunque falle el agente.

**Seguridad:** el agente no tiene acceso a la terminal; solo puede llamar a las 4 herramientas de `agente/herramientas.py`. La clave vive en `sistema/.env`, que está en `.gitignore`: nunca la suba al repositorio ni la comparta en el zip.

## Usar con una IA externa (sin la app)

Cargue la carpeta de cada skill (`sistema/skills/<nombre>/`) en la IA, según el producto que se use, y escriba, por ejemplo:

> Usa la skill y resuelve: 2x + y − z = 8; −3x − y + 2z = −11; −2x + y + 2z = −3

Si la cuenta no permite skills, el plan alterno es pegar el contenido del `SKILL.md` en el chat y ejecutar el script localmente (ver `documentacion/fase-3-tecnologias.md`).

## Documentación

- Planificación completa (fases 1 a 4): [`documentacion/`](documentacion/)
- Batería de evaluación: [`sistema/evaluacion/bateria.md`](sistema/evaluacion/bateria.md)

## Agregar una skill

1. Crear `sistema/skills/<nombre-en-minusculas>/` con `SKILL.md` y `scripts/`.
2. Redactar la `description` indicando **cuándo** debe usarse.
3. Hacer que el script lea un JSON y devuelva un JSON.
4. Añadir pruebas en `sistema/tests/`.
