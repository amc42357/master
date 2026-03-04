#!/usr/bin/env python3
"""
Script de verificación del entorno (US-01).
Comprueba que las dependencias se importan correctamente, que fpdf2 está
disponible para exportación de reportes PDF y que el modelo de pose existe.
"""
import logging
import sys
from pathlib import Path

# Añadir raíz del proyecto para importar config
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


def main():
    errors = []
    try:
        import cv2
        log.info("  [OK] opencv-python (cv2)")
    except ImportError as e:
        errors.append(f"opencv-python: {e}")

    try:
        import mediapipe
        log.info("  [OK] mediapipe")
    except ImportError as e:
        errors.append(f"mediapipe: {e}")

    try:
        import numpy
        log.info("  [OK] numpy")
    except ImportError as e:
        errors.append(f"numpy: {e}")

    try:
        import pandas
        log.info("  [OK] pandas")
    except ImportError as e:
        errors.append(f"pandas: {e}")

    try:
        import matplotlib
        log.info("  [OK] matplotlib")
    except ImportError as e:
        errors.append(f"matplotlib: {e}")

    try:
        import scipy
        log.info("  [OK] scipy")
    except ImportError as e:
        errors.append(f"scipy: {e}")

    try:
        from fpdf import FPDF
        log.info("  [OK] fpdf2 (exportación PDF)")
    except ImportError:
        log.info("  [--] fpdf2 no instalado (opcional: pip install fpdf2 para export_session_report.py)")

    # Modelo de pose (necesario para ejecutar el prototipo)
    try:
        from src import config
        if config.POSE_MODEL_PATH.exists():
            log.info("  [OK] Modelo de pose: %s", config.POSE_MODEL_PATH)
        else:
            errors.append(
                f"Modelo no encontrado: {config.POSE_MODEL_PATH}. "
                "Lite: curl -L 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task' -o models/pose_landmarker.task"
            )
    except Exception as e:
        errors.append(f"Config/modelo: {e}")

    if errors:
        log.error("Errores: %s", errors)
        sys.exit(1)
    log.info("Entorno verificado correctamente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
