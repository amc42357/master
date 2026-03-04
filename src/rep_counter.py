"""
Módulo de lógica de aplicación - Conteo de repeticiones (US-05).
Máquina de estados para detectar ciclos subida/bajada y repeticiones válidas.
"""

from enum import Enum
from typing import Optional

from . import config


class RepState(str, Enum):
    """Estado del ciclo de movimiento."""
    UP = "up"      # Brazo subiendo (ángulo aumentando)
    DOWN = "down"  # Brazo bajando (ángulo disminuyendo)


class RepCounter:
    """
    Contador de repeticiones válidas de abducción de hombro.
    Usa umbrales configurables para detectar ciclos completos.
    """

    def __init__(
        self,
        threshold_valid: float = config.ANGLE_THRESHOLD_VALID_REP,
        threshold_up: float = config.ANGLE_THRESHOLD_UP,
        threshold_down: float = config.ANGLE_THRESHOLD_DOWN,
        min_frames_up: int = config.MIN_FRAMES_UP_BEFORE_COUNT,
        cooldown_frames: int = config.COOLDOWN_FRAMES_AFTER_COUNT,
    ):
        """
        Inicializa el contador.

        Args:
            threshold_valid: Ángulo mínimo para considerar repetición válida.
            threshold_up: Umbral para transición down -> up.
            threshold_down: Umbral para transición up -> down (histeresis).
            min_frames_up: Frames mínimos en estado "arriba" para contar una rep (evita falsos positivos).
            cooldown_frames: Frames de espera tras una rep antes de permitir nueva subida (evita doble conteo).
        """
        self.threshold_valid = threshold_valid
        self.threshold_up = threshold_up
        self.threshold_down = threshold_down
        self.min_frames_up = min_frames_up
        self.cooldown_frames = cooldown_frames

        self._state = RepState.DOWN
        self._count = 0
        self._reached_valid_in_current_cycle = False
        self._feedback_msg = ""
        self._frames_in_up = 0
        self._cooldown_frames_remaining = 0

    @property
    def count(self) -> int:
        """Número de repeticiones válidas completadas."""
        return self._count

    @property
    def state(self) -> RepState:
        """Estado actual del ciclo (up/down)."""
        return self._state

    @property
    def feedback_msg(self) -> str:
        """Mensaje de retroalimentación más reciente."""
        return self._feedback_msg

    def update(self, angle_deg: Optional[float]) -> tuple[RepState, int, str]:
        """
        Actualiza el estado con un nuevo ángulo.

        Args:
            angle_deg: Ángulo actual en grados (None si no hay detección).

        Returns:
            Tupla (estado_actual, conteo, mensaje_feedback).
        """
        self._feedback_msg = ""

        if angle_deg is None:
            return self._state, self._count, self._feedback_msg

        # Cooldown: solo decrece mientras estamos abajo (evita conteos seguidos por ruido)
        if self._state == RepState.DOWN and self._cooldown_frames_remaining > 0:
            self._cooldown_frames_remaining -= 1

        # Transiciones de estado
        if self._state == RepState.DOWN:
            if angle_deg >= self.threshold_up and self._cooldown_frames_remaining == 0:
                self._state = RepState.UP
                self._frames_in_up = 0
                self._reached_valid_in_current_cycle = True
            elif angle_deg >= self.threshold_valid and angle_deg < self.threshold_up:
                self._feedback_msg = "Extienda más el brazo"

        else:  # UP
            self._frames_in_up += 1
            if angle_deg <= self.threshold_down:
                self._state = RepState.DOWN
                if self._reached_valid_in_current_cycle and self._frames_in_up >= self.min_frames_up:
                    self._count += 1
                    self._feedback_msg = "Repetición válida"
                    self._cooldown_frames_remaining = self.cooldown_frames
                self._reached_valid_in_current_cycle = False

        return self._state, self._count, self._feedback_msg

    def reset(self) -> None:
        """Reinicia el contador y el estado."""
        self._state = RepState.DOWN
        self._count = 0
        self._reached_valid_in_current_cycle = False
        self._feedback_msg = ""
        self._frames_in_up = 0
        self._cooldown_frames_remaining = 0
