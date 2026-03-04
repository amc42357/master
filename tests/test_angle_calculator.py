"""Pruebas del módulo angle_calculator."""

import pytest
from src.angle_calculator import angle_between_vectors, calculate_shoulder_abduction_angle


def test_angle_90_degrees():
    """Ángulo de 90° entre vectores perpendiculares."""
    # vertex en (0,0), p1=(1,0), p2=(0,1) -> 90°
    result = angle_between_vectors((1, 0), (0, 0), (0, 1))
    assert abs(result - 90.0) < 0.01


def test_angle_180_degrees():
    """Ángulo de 180° (vectores opuestos)."""
    result = angle_between_vectors((1, 0), (0, 0), (-1, 0))
    assert abs(result - 180.0) < 0.01


def test_angle_zero():
    """Ángulo de 0° (vectores alineados mismo sentido)."""
    result = angle_between_vectors((1, 0), (0, 0), (2, 0))
    assert abs(result - 0.0) < 0.01


def test_calculate_shoulder_abduction_none():
    """Sin coordenadas retorna None."""
    assert calculate_shoulder_abduction_angle(None) is None


def test_calculate_shoulder_abduction_valid():
    """Con coordenadas válidas retorna ángulo."""
    coords = {
        "hip": (0.5, 0.7),
        "shoulder": (0.5, 0.5),
        "elbow": (0.5, 0.3),
    }
    result = calculate_shoulder_abduction_angle(coords)
    assert result is not None
    assert 0 <= result <= 180
