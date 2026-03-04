"""Pruebas del módulo session_logger."""

import csv
import tempfile
from pathlib import Path

import pytest

from src.session_logger import SessionLogger


EXPECTED_HEADER = [
    "timestamp",
    "frame_id",
    "shoulder_x", "shoulder_y",
    "elbow_x", "elbow_y",
    "hip_x", "hip_y",
    "angle_deg",
    "rep_state",
    "feedback_msg",
]


def test_start_writes_header_and_returns_path():
    """start() crea el archivo con cabecera correcta y devuelve la ruta."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        logger = SessionLogger(output_dir=out_dir)
        path = logger.start(filename="test_sesion.csv")
        logger.stop()

        assert path == out_dir / "test_sesion.csv"
        assert path.exists()
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            row = next(reader)
            assert row == EXPECTED_HEADER


def test_log_writes_rows_with_expected_columns():
    """log() escribe filas con el formato esperado."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        logger = SessionLogger(output_dir=out_dir)
        path = logger.start(filename="test_log.csv")

        coords = {
            "shoulder": (0.4, 0.3),
            "elbow": (0.35, 0.4),
            "hip": (0.41, 0.52),
        }
        logger.log(coords, 45.2, "down", "")
        logger.log(coords, 72.0, "up", "Repetición válida")
        logger.stop()

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["rep_state"] == "down"
        assert rows[0]["feedback_msg"] == ""
        assert rows[1]["rep_state"] == "up"
        assert "Repetición válida" in rows[1]["feedback_msg"]
        assert float(rows[0]["angle_deg"]) == 45.2
        assert int(rows[0]["frame_id"]) == 0
        assert int(rows[1]["frame_id"]) == 1


def test_log_without_start_does_nothing():
    """Llamar log() sin start() no escribe ni falla."""
    with tempfile.TemporaryDirectory() as tmp:
        logger = SessionLogger(output_dir=Path(tmp))
        logger.log({"shoulder": (0, 0), "elbow": (0, 0), "hip": (0, 0)}, 0.0, "down", "")
        logger.stop()
        # No se creó ningún archivo
        assert len(list(Path(tmp).iterdir())) == 0


def test_log_with_none_coords_uses_zeros():
    """log() con coords=None escribe ceros en coordenadas."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        logger = SessionLogger(output_dir=out_dir)
        path = logger.start(filename="test_none.csv")
        logger.log(None, None, "down", "")
        logger.stop()

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            row = next(reader)
        assert row["shoulder_x"] == "0.0000"
        assert row["angle_deg"] == ""


def test_stop_closes_file_and_prevents_further_log():
    """stop() cierra el archivo; log() posterior no escribe."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        logger = SessionLogger(output_dir=out_dir)
        path = logger.start(filename="test_stop.csv")
        logger.log({"shoulder": (0, 0), "elbow": (0, 0), "hip": (0, 0)}, 10.0, "down", "")
        logger.stop()
        logger.log({"shoulder": (0, 0), "elbow": (0, 0), "hip": (0, 0)}, 20.0, "up", "")

        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        # Cabecera + 1 fila (la segunda log no debe escribirse)
        assert len(rows) == 2


def test_context_manager():
    """SessionLogger funciona como context manager."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        with SessionLogger(output_dir=out_dir) as logger:
            path = logger.start(filename="ctx.csv")
            logger.log({"shoulder": (0.5, 0.5), "elbow": (0.5, 0.4), "hip": (0.5, 0.6)}, 90.0, "up", "")
        assert path.exists()
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        assert len(rows) == 2  # header + 1 data row
