# Sistema de Rehabilitación Motriz - Visión por Computadora
# Imagen base Python 3.11 (Bookworm para compatibilidad de paquetes)
FROM python:3.11-slim-bookworm

# Instalar dependencias del sistema para OpenCV (GUI y video) y curl para descargar modelo
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelo de pose (MediaPipe pose_landmarker_lite) durante el build
RUN mkdir -p /app/models \
    && curl -sL 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task' \
    -o /app/models/pose_landmarker.task

# Copiar código fuente
COPY src/ ./src/
COPY scripts/ ./scripts/

# Directorio para datos (sesiones, CSVs)
RUN mkdir -p /app/data

# Comando por defecto: ejecutar el prototipo
# En Linux con cámara: docker run --device=/dev/video0 ...
# Para scripts de análisis: docker run ... python scripts/plot_angle_evolution.py
CMD ["python", "src/main.py"]
