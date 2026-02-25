"""Pruebas del módulo rep_counter."""

import pytest
from src.rep_counter import RepCounter, RepState


def test_initial_state():
    """Estado inicial: down, count=0."""
    counter = RepCounter(threshold_valid=60, threshold_up=60, threshold_down=45)
    assert counter.state == RepState.DOWN
    assert counter.count == 0


def test_count_increments_on_full_cycle():
    """Una repetición válida incrementa el contador (sin debounce para test rápido)."""
    counter = RepCounter(
        threshold_valid=60, threshold_up=60, threshold_down=45,
        min_frames_up=0, cooldown_frames=0,
    )

    # Subir por encima de 60
    counter.update(30)
    counter.update(50)
    counter.update(70)  # pasa a UP, reached_valid=True
    counter.update(80)

    # Bajar por debajo de 45
    counter.update(50)
    counter.update(40)  # pasa a DOWN, count+=1
    assert counter.count == 1


def test_reset():
    """Reset vuelve al estado inicial."""
    counter = RepCounter()
    counter.update(70)
    counter.update(40)
    counter.reset()
    assert counter.count == 0
    assert counter.state == RepState.DOWN
