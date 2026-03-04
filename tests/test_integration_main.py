"""Test de integración: ejecutar el pipeline con --video --headless --accept-consent."""

import subprocess
import sys
from pathlib import Path

import pytest

# Raíz del proyecto (rehab_cv)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEST_VIDEO = DATA_DIR / "test_video.mp4"


def _ensure_test_video():
    """Crea data/test_video.mp4 si no existe (ejecutando create_test_video.py)."""
    if TEST_VIDEO.exists():
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "create_test_video.py")],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert r.returncode == 0, f"create_test_video falló: {r.stderr}"


@pytest.mark.skipif(
    not (PROJECT_ROOT / "models" / "pose_landmarker.task").exists(),
    reason="Modelo pose_landmarker.task no encontrado (ejecutar descarga o build Docker)",
)
def test_main_headless_video_exits_successfully():
    """El pipeline con --video --headless --accept-consent termina sin excepción."""
    _ensure_test_video()
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.main",
            "--video",
            str(TEST_VIDEO),
            "--headless",
            "--accept-consent",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"main falló con stderr: {result.stderr!r} stdout: {result.stdout!r}"
    )
