"""
Módulo de captura de video (US-02).
Captura frames desde cámara web usando OpenCV.
"""

import cv2
from pathlib import Path
from typing import Generator, Optional

from . import config


class VideoCapture:
    """Captura de video desde cámara web o archivo de video."""

    def __init__(
        self,
        source: int | str = 0,
        width: int = config.CAMERA_WIDTH,
        height: int = config.CAMERA_HEIGHT,
        fps: int = config.CAMERA_FPS,
    ):
        """
        Inicializa la captura de video.

        Args:
            source: Índice de cámara (0 por defecto) o ruta a archivo de video.
            width: Ancho en píxeles (720p+).
            height: Alto en píxeles.
            fps: Fotogramas por segundo deseados.
        """
        self._source = source
        self._cap = cv2.VideoCapture(source)
        if not self._cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la fuente de video: {source}")

        # Solo configurar resolución si es cámara (no archivo)
        if isinstance(source, int):
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self._cap.set(cv2.CAP_PROP_FPS, fps)

        self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def read(self) -> tuple[bool, Optional[bytes]]:
        """
        Lee un frame de video.

        Returns:
            Tupla (éxito, frame). frame es None si no hay más frames.
        """
        ret, frame = self._cap.read()
        if not ret:
            return False, None
        return True, frame

    def frames(self) -> Generator[bytes, None, None]:
        """Generador de frames hasta que se cierre o no haya más."""
        while True:
            ret, frame = self.read()
            if not ret or frame is None:
                break
            yield frame

    def release(self) -> None:
        """Libera el recurso de la cámara."""
        self._cap.release()

    def __enter__(self) -> "VideoCapture":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
