"""
Módulo de registro de sesión en CSV (US-10).
Exporta timestamp, ángulo, estado de repetición y mensaje de feedback por frame/evento.
"""

import csv
from pathlib import Path
from typing import Optional
import time

from . import config


class SessionLogger:
    """Registra datos de la sesión en un archivo CSV."""

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Inicializa el logger.

        Args:
            output_dir: Directorio donde guardar el CSV. Por defecto config.DATA_DIR.
        """
        self._output_dir = output_dir or config.DATA_DIR
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._file = None
        self._writer = None
        self._start_time = None
        self._frame_id = 0

    def start(self, filename: Optional[str] = None) -> Path:
        """
        Inicia el registro creando el archivo CSV.

        Args:
            filename: Nombre del archivo. Por defecto sesion_YYYYMMDD_HHMMSS.csv

        Returns:
            Ruta del archivo creado.
        """
        if filename is None:
            from datetime import datetime
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sesion_{ts}.csv"

        path = self._output_dir / filename
        self._file = open(path, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        self._writer.writerow([
            "timestamp",
            "frame_id",
            "shoulder_x", "shoulder_y",
            "elbow_x", "elbow_y",
            "hip_x", "hip_y",
            "angle_deg",
            "rep_state",
            "feedback_msg",
        ])
        self._start_time = time.perf_counter()
        self._frame_id = 0
        return path

    def log(
        self,
        coords: Optional[dict],
        angle_deg: Optional[float],
        rep_state: str,
        feedback_msg: str,
    ) -> None:
        """
        Registra una fila en el CSV.

        Args:
            coords: Dict con shoulder, elbow, hip (cada uno (x, y)).
            angle_deg: Ángulo calculado.
            rep_state: "up" o "down".
            feedback_msg: Mensaje de retroalimentación.
        """
        if self._writer is None:
            return

        elapsed = time.perf_counter() - self._start_time if self._start_time else 0

        if coords:
            sx, sy = coords.get("shoulder", (0, 0))
            ex, ey = coords.get("elbow", (0, 0))
            hx, hy = coords.get("hip", (0, 0))
        else:
            sx = sy = ex = ey = hx = hy = 0

        self._writer.writerow([
            f"{elapsed:.3f}",
            self._frame_id,
            f"{sx:.4f}", f"{sy:.4f}",
            f"{ex:.4f}", f"{ey:.4f}",
            f"{hx:.4f}", f"{hy:.4f}",
            f"{angle_deg:.1f}" if angle_deg is not None else "",
            rep_state,
            feedback_msg,
        ])
        self._frame_id += 1
        # Flush cada 30 frames (~1 s) para no perder datos si la app se cierra
        if self._frame_id % 30 == 0 and self._file:
            self._file.flush()

    def stop(self) -> None:
        """Cierra el archivo y finaliza el registro."""
        if self._file:
            self._file.close()
            self._file = None
        self._writer = None

    def __enter__(self) -> "SessionLogger":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()
