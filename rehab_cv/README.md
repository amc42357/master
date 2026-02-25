# Sistema de Rehabilitación Motriz - Visión por Computadora

Prototipo de software basado en visión por computadora y aprendizaje automático para asistir la ejecución domiciliaria de ejercicios de rehabilitación de hombro (abducción) en pacientes post-ACV.

**Tecnologías:** Python, OpenCV, MediaPipe, NumPy

## Características

- **Captura de video** en tiempo real desde cámara web (720p)
- **Detección de pose** con MediaPipe (33 landmarks anatómicos)
- **Cálculo de ángulo** de abducción del hombro (cadera–hombro–codo)
- **Conteo automático** de repeticiones válidas con umbrales configurables
- **Retroalimentación visual** en tiempo real ("Levante más el brazo", "Repetición válida")
- **Exportación CSV** de sesiones para análisis posterior

## Requisitos

- Python 3.9+
- Cámara web (o archivo de video para pruebas)
- **Modelo de pose:** Por defecto se usa **pose_landmarker_lite** (más rápido; es el que usa el MVP y la validación del documento). Opcionalmente puede usarse **pose_landmarker full** (más preciso, más pesado) con `--model full`. Descarga manual: lite → `models/pose_landmarker.task`, full → `models/pose_landmarker_full.task` (ver [Instalación](#instalación)).

## Instalación

### Entorno local (recomendado para uso con cámara)

```bash
cd rehab_cv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Modelo de pose (lite por defecto)

El prototipo usa **pose_landmarker_lite** por defecto (mejor rendimiento). Opcionalmente, para mayor precisión:

```bash
# Lite (por defecto) — ya incluido en Docker
curl -L 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task' -o models/pose_landmarker.task

# Full (opcional) — usar con --model full
curl -L 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker/float16/1/pose_landmarker.task' -o models/pose_landmarker_full.task
```

### Verificar entorno

```bash
python scripts/verify_env.py
```

## Uso

### Ejecutar con cámara web

```bash
python src/main.py
```

### Opciones

- `--video ruta/video.mp4` — Probar con archivo de video (sin cámara)
- `--camera 0` — Índice de cámara (default: 0)
- `--record` — Registrar sesión en CSV en `data/`
- `--arm left|right` — Brazo a analizar (default: right)
- `--headless` — Modo sin ventana (para Docker/CI)
- `--accept-consent` — Asumir consentimiento (para scripts no interactivos)
- `--model lite|full` — Modelo de pose (default: lite)

Por defecto la interfaz usa OpenCV (ventana única con overlay). Para usar Dear PyGui (ventanas separadas de video y métricas), define `REHAB_USE_DPG=1` antes de ejecutar.

### Ejemplo con registro (guardar sesión en CSV)

**Importante:** Para guardar los datos de la sesión (ángulos, repeticiones) debe usar `--record`.
Cuando está grabando, verá un punto rojo y "GRABANDO" en la esquina del panel.

```bash
python src/main.py --record
```

El archivo CSV se guarda en `data/sesion_YYYYMMDD_HHMMSS.csv`. Pulse **q** o **ESC** para salir.

### Script de análisis (gráfico de ángulo)

```bash
python scripts/plot_angle_evolution.py data/sesion_YYYYMMDD_HHMMSS.csv -o grafico.png
```

O con el CSV de ejemplo:

```bash
python scripts/plot_angle_evolution.py
```

### Script de validación (MAE, precisión)

Para comparar con datos de referencia (goniómetro, conteo humano) y generar informe:

```bash
python scripts/analyze_validation.py data/sesion_YYYYMMDD_HHMMSS.csv [referencia.csv] -o data
```

El CSV de referencia debe tener columnas: `rep_num`, `angle_goniometer`, `valid_human`:

```csv
rep_num,angle_goniometer,valid_human
1,92.5,1
2,88.0,1
```

Genera: informe Markdown, gráfico de dispersión (sistema vs goniómetro) y series temporales.

### Exportación a PDF (resumen de sesión)

```bash
python scripts/export_session_report.py data/sesion_YYYYMMDD_HHMMSS.csv -o reporte.pdf
```

## Docker

### Construir imagen

La imagen descarga el modelo de pose (pose_landmarker_lite) durante el build; no es necesario tener `models/` localmente.

```bash
docker build -t rehab-cv .
```

### Ejecutar (modo headless, sin ventana - para Docker/CI)

```bash
docker run --rm -v $(pwd)/data:/app/data rehab-cv python src/main.py --video /app/data/test_video.mp4 --headless
```

### Ejecutar (Linux con cámara)

```bash
docker run --rm -it --device=/dev/video0:/dev/video0 -v $(pwd)/data:/app/data rehab-cv
```

### Con docker-compose

```bash
docker-compose up --build
```

**Nota:** En macOS, el acceso a la cámara desde Docker es limitado. Use `--headless --video archivo.mp4` para probar en Docker, o ejecute localmente con `python src/main.py` para uso con cámara.

### Scripts de análisis en Docker (sin cámara)

```bash
docker run --rm -v $(pwd)/data:/app/data rehab-cv python scripts/plot_angle_evolution.py
```

## Estructura del proyecto

```
rehab_cv/
├── src/
│   ├── main.py            # Punto de entrada
│   ├── config.py          # Configuración y umbrales
│   ├── capture.py         # Captura de video (OpenCV)
│   ├── pose_detector.py   # Detección de pose (MediaPipe)
│   ├── angle_calculator.py# Cálculo geométrico del ángulo
│   ├── rep_counter.py     # Máquina de estados, conteo
│   ├── gui.py             # Interfaz gráfica
│   └── session_logger.py  # Exportación CSV
├── scripts/
│   ├── verify_env.py      # Verificación de dependencias
│   ├── plot_angle_evolution.py  # Gráfico de ángulo
│   ├── analyze_validation.py   # Análisis MAE, precisión, informe
│   └── export_session_report.py  # Exportar resumen a PDF
├── data/                  # Sesiones CSV
├── tests/
├── docs/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Criterios de validación (proyecto)

- **MAE angular:** ≤ 5° vs goniómetro
- **Precisión de conteo:** ≥ 95%
- **Latencia:** < 150 ms

## Referencia

Proyecto del Seminario de Innovación en IA (UNIR). Documentación completa en `../proyecto.md` y anexos.
