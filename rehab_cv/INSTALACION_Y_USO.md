# Instalación y uso – rehab_cv

Guía paso a paso para instalar y usar el sistema de rehabilitación motriz con visión por computadora.

---

## 1. Requisitos

- **Python** 3.9 o superior  
- **Cámara web** (o archivo de video para pruebas sin cámara)  
- **Sistema operativo:** macOS, Linux o Windows  

---

## 2. Instalación

### 2.1 Clonar o descargar el proyecto

Si tienes el repositorio en GitHub:

```bash
git clone https://github.com/amc42357/master.git rehab_cv
cd rehab_cv
```

O descomprime el código en una carpeta y entra en ella:

```bash
cd rehab_cv
```

### 2.2 Crear el entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate    # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2.3 Modelo de pose (MediaPipe)

El modelo **lite** suele venir ya en el repo. Si no existe `models/pose_landmarker.task`, descárgalo:

```bash
mkdir -p models
curl -L 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task' -o models/pose_landmarker.task
```

Opcional (más preciso, más pesado):

```bash
curl -L 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker/float16/1/pose_landmarker.task' -o models/pose_landmarker_full.task
```

### 2.4 Verificar que todo está listo

```bash
python scripts/verify_env.py
```

Debe mostrar que OpenCV, MediaPipe, el modelo, etc. están correctos.

---

## 3. Uso básico

### 3.1 Ejecutar con cámara (sin grabar)

```bash
source venv/bin/activate   # si no está activado
python src/main.py
```

- Colócate frente a la cámara (~2 m, buena luz).
- Verás el esqueleto superpuesto, el ángulo del brazo y el contador de repeticiones.
- Para salir: **q** o **ESC**.

### 3.2 Ejecutar y grabar la sesión (CSV)

Para guardar ángulos y repeticiones en un CSV:

```bash
python src/main.py --record
```

- Aparecerá **GRABANDO** en pantalla.
- El archivo se guarda en `data/sesion_YYYYMMDD_HHMMSS.csv`.
- Salir: **q** o **ESC**.

### 3.3 Protocolo: 3 series × 10 repeticiones y metrónomo

El sistema está preparado para el protocolo de validación:

- **Objetivo:** 3 series de 10 repeticiones de abducción de hombro.
- **Ritmo:** 1 repetición cada 3 segundos (metrónomo con beep cada 3 s).
- En pantalla verás: *Serie X de 3* y *Repetición Y de 10*.

Comando recomendado para una sesión completa con grabación:

```bash
python src/main.py --record
```

Para desactivar el metrónomo:

```bash
python src/main.py --record --no-metronome
```

### 3.4 Consentimiento informado

La primera vez que ejecutes la aplicación se mostrará un mensaje de consentimiento. Acepta con **S** para continuar. El estado se guarda en `~/.rehab_cv/`.

---

## 4. Opciones de línea de comandos

| Opción | Descripción |
|--------|-------------|
| `--record` | Graba la sesión en CSV en `data/` |
| `--arm left` o `--arm right` | Brazo a analizar (por defecto: right) |
| `--camera 0` | Índice de cámara (0 = por defecto) |
| `--video ruta/video.mp4` | Usar archivo de video en lugar de cámara |
| `--no-metronome` | Desactiva el beep cada 3 segundos |
| `--model full` | Usa el modelo de pose “full” (más preciso, más lento) |
| `--headless` | Sin ventana (para Docker/scripts) |
| `--accept-consent` | Omite la pregunta de consentimiento (scripts) |

Ejemplos:

```bash
# Brazo izquierdo, sin metrónomo
python src/main.py --record --arm left --no-metronome

# Probar con un video (sin cámara)
python src/main.py --video data/test_video.mp4 --record
```

---

## 5. Después de la sesión: análisis

### Gráfico de evolución del ángulo

```bash
python scripts/plot_angle_evolution.py data/sesion_YYYYMMDD_HHMMSS.csv -o grafico.png
```

### Análisis de validación (MAE, precisión vs. goniómetro)

Si tienes un CSV de referencia con columnas `rep_num`, `angle_goniometer`, `valid_human`:

```bash
python scripts/analyze_validation.py data/sesion_YYYYMMDD_HHMMSS.csv data/referencia.csv -o data
```

### Exportar resumen a PDF

```bash
python scripts/export_session_report.py data/sesion_YYYYMMDD_HHMMSS.csv -o reporte.pdf
```

---

## 6. Docker (opcional)

Construir y ejecutar con Docker:

```bash
docker build -t rehab-cv .
docker run --rm -it -v $(pwd)/data:/app/data rehab-cv
```

Para usar cámara en Linux:

```bash
docker run --rm -it --device=/dev/video0:/dev/video0 -v $(pwd)/data:/app/data rehab-cv
```

En macOS el acceso a la cámara desde Docker es limitado; se recomienda ejecutar localmente con `python src/main.py`.

---

## 7. Estructura del proyecto

```
rehab_cv/
├── src/
│   ├── main.py          # Punto de entrada
│   ├── config.py        # Configuración
│   ├── capture.py       # Captura de video
│   ├── pose_detector.py # Detección de pose (MediaPipe)
│   ├── angle_calculator.py
│   ├── rep_counter.py
│   ├── gui.py
│   └── session_logger.py
├── scripts/             # Análisis y utilidades
├── data/                # CSVs de sesión y salidas
├── models/              # Modelo de pose
├── requirements.txt
├── README.md
└── INSTALACION_Y_USO.md # Este documento
```

---

## 8. Criterios de validación (referencia)

- **MAE angular:** ≤ 5° frente a goniómetro  
- **Precisión de conteo:** ≥ 95%  
- **Latencia:** < 150 ms  

Para más detalles del protocolo y limitaciones conocidas, ver `data/PROTOCOLO_SUJETO1.md` y `KNOWN_ISSUES.md`.
