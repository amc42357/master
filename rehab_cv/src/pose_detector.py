"""
Módulo de detección de pose (US-03).
Usa MediaPipe Pose Landmarker (Tasks API) para estimar 33 landmarks anatómicos en 2D.
"""

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python.vision import (
    PoseLandmarker,
    PoseLandmarkerOptions,
    RunningMode,
    PoseLandmarksConnections,
)
from mediapipe.tasks.python import BaseOptions
from pathlib import Path
from typing import Optional

from . import config

def _get_connections():
    """Obtiene las conexiones de pose (tuplas de índices)."""
    try:
        conn = PoseLandmarksConnections.POSE_LANDMARKS
        return [(c.start, c.end) for c in conn]
    except Exception:
        return [(11, 12), (11, 13), (13, 15), (12, 14), (14, 16), (11, 23), (12, 24),
                (23, 24), (23, 25), (25, 27), (24, 26), (26, 28)]


class PoseDetector:
    """Detector de pose humana usando MediaPipe Pose Landmarker."""

    def __init__(
        self,
        model_path: Optional[Path] = None,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        """
        Inicializa el detector de pose.

        Args:
            model_path: Ruta al modelo .task. Por defecto config.POSE_MODEL_PATH.
            min_detection_confidence: Umbral mínimo para detección inicial.
            min_tracking_confidence: Umbral mínimo para tracking entre frames.
        """
        path = model_path or config.POSE_MODEL_PATH
        if not path.exists():
            raise FileNotFoundError(
                f"Modelo no encontrado: {path}. "
                "Lite: curl -L 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task' -o models/pose_landmarker.task . "
                "Full: curl -L 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker/float16/1/pose_landmarker.task' -o models/pose_landmarker_full.task"
            )

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(path)),
            running_mode=RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self._landmarker = PoseLandmarker.create_from_options(options)
        self._frame_timestamp_ms = 0

    def process(self, frame: np.ndarray) -> Optional[list]:
        """
        Procesa un frame y retorna los landmarks detectados.

        Args:
            frame: Imagen BGR (formato OpenCV).

        Returns:
            Lista de landmarks normalizados o None si no hay detección.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._landmarker.detect_for_video(mp_image, self._frame_timestamp_ms)
        self._frame_timestamp_ms += 33  # ~30 FPS

        if not result.pose_landmarks:
            return None
        return result.pose_landmarks[0]

    def _draw_landmarks_cv(
        self, frame: np.ndarray, landmarks
    ) -> np.ndarray:
        """Dibuja landmarks con OpenCV (compatible con todas las versiones de MediaPipe)."""
        h, w = frame.shape[:2]
        connections = _get_connections()

        def to_px(x, y):
            return (int(x * w), int(y * h))

        for i, lm in enumerate(landmarks):
            px, py = to_px(lm.x, lm.y)
            if 0 <= px < w and 0 <= py < h:
                cv2.circle(frame, (px, py), 4, (0, 255, 0), -1)
        for (i, j) in connections:
            if i < len(landmarks) and j < len(landmarks):
                pt1 = to_px(landmarks[i].x, landmarks[i].y)
                pt2 = to_px(landmarks[j].x, landmarks[j].y)
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
        return frame

    def draw_landmarks(
        self,
        frame: np.ndarray,
        landmarks,
    ) -> np.ndarray:
        """
        Dibuja landmarks y conexiones sobre el frame.

        Args:
            frame: Imagen BGR donde dibujar.
            landmarks: Resultado de process() (lista de NormalizedLandmark).

        Returns:
            Frame con el esqueleto superpuesto.
        """
        if landmarks is None:
            return frame
        return self._draw_landmarks_cv(frame.copy(), landmarks)

    def get_landmark_coords(
        self,
        landmarks,
        arm: str = None,
    ) -> Optional[dict]:
        """
        Extrae coordenadas normalizadas (x, y) de hombro, codo y cadera.

        Args:
            landmarks: Resultado de process() (lista de landmarks).
            arm: "right" o "left". Por defecto usa config.DEFAULT_ARM.

        Returns:
            Dict con shoulder, elbow, hip (cada uno (x, y)) o None.
        """
        if landmarks is None or len(landmarks) < 33:
            return None
        arm = arm or config.DEFAULT_ARM

        if arm == "right":
            shoulder_idx = config.LANDMARK_SHOULDER_RIGHT
            elbow_idx = config.LANDMARK_ELBOW_RIGHT
            hip_idx = config.LANDMARK_HIP_RIGHT
        else:
            shoulder_idx = config.LANDMARK_SHOULDER_LEFT
            elbow_idx = config.LANDMARK_ELBOW_LEFT
            hip_idx = config.LANDMARK_HIP_LEFT

        def pt(idx):
            lm = landmarks[idx]
            return (lm.x, lm.y)

        return {
            "shoulder": pt(shoulder_idx),
            "elbow": pt(elbow_idx),
            "hip": pt(hip_idx),
        }

    def close(self) -> None:
        """Libera recursos."""
        self._landmarker.close()

    def __enter__(self) -> "PoseDetector":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
