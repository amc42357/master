"""
Módulo de cálculo geométrico (US-04).
Calcula el ángulo de abducción del hombro (cadera-hombro-codo) usando geometría vectorial.
"""

import math
from typing import Optional


def angle_between_vectors(
    p1: tuple[float, float],
    vertex: tuple[float, float],
    p2: tuple[float, float],
) -> float:
    """
    Calcula el ángulo en grados en el vértice formado por p1-vertex-p2.

    El ángulo de abducción del hombro usa:
    - p1: cadera (punto inferior)
    - vertex: hombro (vértice)
    - p2: codo (punto superior cuando el brazo está elevado)

    Args:
        p1, vertex, p2: Coordenadas (x, y) normalizadas.

    Returns:
        Ángulo en grados [0, 180].
    """
    v1 = (p1[0] - vertex[0], p1[1] - vertex[1])
    v2 = (p2[0] - vertex[0], p2[1] - vertex[1])

    dot = v1[0] * v2[0] + v1[1] * v2[1]
    len1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    len2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    if len1 < 1e-6 or len2 < 1e-6:
        return 0.0

    cos_angle = max(-1.0, min(1.0, dot / (len1 * len2)))
    return math.degrees(math.acos(cos_angle))


def calculate_shoulder_abduction_angle(coords: Optional[dict]) -> Optional[float]:
    """
    Calcula el ángulo de abducción del hombro a partir de las coordenadas.

    Usa la geometría: ángulo en el hombro entre el vector hombro-cadera
    y el vector hombro-codo.

    Args:
        coords: Dict con "hip", "shoulder", "elbow" (cada uno (x, y)).

    Returns:
        Ángulo en grados o None si coords es inválido.
    """
    if coords is None:
        return None
    hip = coords.get("hip")
    shoulder = coords.get("shoulder")
    elbow = coords.get("elbow")
    if not all([hip, shoulder, elbow]):
        return None

    return angle_between_vectors(hip, shoulder, elbow)
