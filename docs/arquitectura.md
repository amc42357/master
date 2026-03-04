# Arquitectura del Sistema

## Pipeline de procesamiento

```
[Cámara Web] → capture.py → pose_detector.py → angle_calculator.py
                                    ↓
                    rep_counter.py ← (ángulo por frame)
                                    ↓
            gui.py ← (estado, conteo, feedback)
                                    ↓
            [Ventana OpenCV] + [CSV opcional]
```

## Módulos

| Módulo | Responsabilidad |
|--------|-----------------|
| `capture.py` | Captura de frames desde cámara o archivo de video |
| `pose_detector.py` | MediaPipe Pose, 33 landmarks, dibujo del esqueleto |
| `angle_calculator.py` | Geometría vectorial: ángulo cadera-hombro-codo |
| `rep_counter.py` | Máquina de estados (up/down), umbrales, conteo |
| `gui.py` | Panel de métricas, área de feedback, render |
| `session_logger.py` | Exportación CSV (timestamp, ángulo, estado, feedback) |

## Formato CSV de sesión

| Columna | Descripción |
|---------|-------------|
| timestamp | Tiempo en segundos desde inicio |
| frame_id | ID del frame |
| shoulder_x, shoulder_y | Coordenadas normalizadas del hombro |
| elbow_x, elbow_y | Coordenadas del codo |
| hip_x, hip_y | Coordenadas de la cadera |
| angle_deg | Ángulo de abducción en grados |
| rep_state | "up" o "down" |
| feedback_msg | Mensaje mostrado (vacío si no aplica) |
