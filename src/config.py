"""
Configuración del sistema de rehabilitación motriz.
Tipada y validada con Pydantic; umbrales, resolución y rutas según el protocolo.
"""

from pathlib import Path

from pydantic import BaseModel, Field, computed_field


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


class Settings(BaseModel):
    """Configuración de la aplicación. Atributos inmutables."""

    model_config = {"frozen": True}

    # Resolución de captura (720p o superior)
    CAMERA_WIDTH: int = 1280
    CAMERA_HEIGHT: int = 720
    CAMERA_FPS: int = 30

    # Umbrales para conteo de repeticiones (abducción de hombro)
    ANGLE_THRESHOLD_VALID_REP: float = 60.0
    ANGLE_THRESHOLD_UP: float = 60.0
    ANGLE_THRESHOLD_DOWN: float = 45.0
    # Estabilidad: mínimo frames en "arriba" para contar rep; cooldown tras cada rep
    MIN_FRAMES_UP_BEFORE_COUNT: int = 12
    COOLDOWN_FRAMES_AFTER_COUNT: int = 20

    # MediaPipe: índices de landmarks (33 puntos)
    LANDMARK_SHOULDER_RIGHT: int = 12
    LANDMARK_ELBOW_RIGHT: int = 14
    LANDMARK_HIP_RIGHT: int = 24
    LANDMARK_SHOULDER_LEFT: int = 11
    LANDMARK_ELBOW_LEFT: int = 13
    LANDMARK_HIP_LEFT: int = 23

    DEFAULT_ARM: str = "right"

    # Protocolo de validación (3 series × 10 repeticiones, ritmo 1 rep cada 3 s)
    NUM_SERIES: int = 3
    REPS_PER_SERIES: int = 10
    METRONOME_INTERVAL_SEC: float = 3.0

    PROJECT_ROOT: Path = Field(default_factory=_project_root)

    @computed_field
    @property
    def DATA_DIR(self) -> Path:
        return self.PROJECT_ROOT / "data"

    @computed_field
    @property
    def MODELS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "models"

    @computed_field
    @property
    def POSE_MODEL_PATH(self) -> Path:
        return self.MODELS_DIR / "pose_landmarker.task"

    @computed_field
    @property
    def POSE_MODEL_FULL_PATH(self) -> Path:
        return self.MODELS_DIR / "pose_landmarker_full.task"


# Instancia global
_settings = Settings()

# Exponer atributos en el módulo para "from . import config" / "from src import config"
CAMERA_WIDTH = _settings.CAMERA_WIDTH
CAMERA_HEIGHT = _settings.CAMERA_HEIGHT
CAMERA_FPS = _settings.CAMERA_FPS
ANGLE_THRESHOLD_VALID_REP = _settings.ANGLE_THRESHOLD_VALID_REP
ANGLE_THRESHOLD_UP = _settings.ANGLE_THRESHOLD_UP
ANGLE_THRESHOLD_DOWN = _settings.ANGLE_THRESHOLD_DOWN
MIN_FRAMES_UP_BEFORE_COUNT = _settings.MIN_FRAMES_UP_BEFORE_COUNT
COOLDOWN_FRAMES_AFTER_COUNT = _settings.COOLDOWN_FRAMES_AFTER_COUNT
LANDMARK_SHOULDER_RIGHT = _settings.LANDMARK_SHOULDER_RIGHT
LANDMARK_ELBOW_RIGHT = _settings.LANDMARK_ELBOW_RIGHT
LANDMARK_HIP_RIGHT = _settings.LANDMARK_HIP_RIGHT
LANDMARK_SHOULDER_LEFT = _settings.LANDMARK_SHOULDER_LEFT
LANDMARK_ELBOW_LEFT = _settings.LANDMARK_ELBOW_LEFT
LANDMARK_HIP_LEFT = _settings.LANDMARK_HIP_LEFT
DEFAULT_ARM = _settings.DEFAULT_ARM
NUM_SERIES = _settings.NUM_SERIES
REPS_PER_SERIES = _settings.REPS_PER_SERIES
METRONOME_INTERVAL_SEC = _settings.METRONOME_INTERVAL_SEC
PROJECT_ROOT = _settings.PROJECT_ROOT
DATA_DIR = _settings.DATA_DIR
MODELS_DIR = _settings.MODELS_DIR
POSE_MODEL_PATH = _settings.POSE_MODEL_PATH
POSE_MODEL_FULL_PATH = _settings.POSE_MODEL_FULL_PATH

# Alias para código que usa "config" como objeto (ej. config.CAMERA_WIDTH)
config = _settings
