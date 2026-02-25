"""
Módulo de consentimiento informado (proyecto.md 5.3).
Muestra mensaje de consentimiento la primera vez que el usuario inicia la aplicación.
"""

import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)

import cv2
import numpy as np

CONSENT_DIR = Path.home() / ".rehab_cv"
CONSENT_FILE = CONSENT_DIR / "consent_given"

CONSENT_TEXT = """
CONSENTIMIENTO INFORMADO

Este sistema procesa video de su cámara para medir ángulos
y contar repeticiones durante ejercicios de rehabilitación.

- Todo el procesamiento es LOCAL (no se envía a internet).
- Los datos se guardan únicamente si activa --record.
- Puede retirar su consentimiento en cualquier momento.

¿Acepta participar?

[S] Acepto    [N] No acepto
"""


def consent_already_given() -> bool:
    """Comprueba si el usuario ya aceptó el consentimiento."""
    return CONSENT_FILE.exists()


def save_consent() -> None:
    """Guarda que el usuario aceptó el consentimiento."""
    CONSENT_DIR.mkdir(parents=True, exist_ok=True)
    CONSENT_FILE.write_text("1", encoding="utf-8")


def show_consent_gui() -> bool:
    """
    Muestra ventana OpenCV con el consentimiento.
    Retorna True si acepta, False si rechaza.
    """
    width, height = 600, 400
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (45, 45, 45)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    color = (255, 255, 255)
    line_height = 25
    y = 40

    for line in CONSENT_TEXT.strip().split("\n"):
        if line.strip():
            cv2.putText(img, line.strip(), (20, y), font, font_scale, color, 1)
        y += line_height

    cv2.putText(img, "S = Acepto  |  N = No acepto", (20, height - 30), font, 0.6, (0, 255, 0), 2)
    cv2.namedWindow("Consentimiento informado", cv2.WINDOW_NORMAL)
    cv2.imshow("Consentimiento informado", img)

    while True:
        key = cv2.waitKey(100) & 0xFF
        if key == ord("s") or key == ord("S"):
            cv2.destroyWindow("Consentimiento informado")
            return True
        if key == ord("n") or key == ord("N") or key == 27:
            cv2.destroyWindow("Consentimiento informado")
            return False


def show_consent_console() -> bool:
    """
    Muestra consentimiento en consola.
    Retorna True si acepta, False si rechaza.
    """
    print("\n" + "=" * 60)
    print("CONSENTIMIENTO INFORMADO")
    print("=" * 60)
    print("""
Este sistema procesa video de su cámara para medir ángulos
y contar repeticiones durante ejercicios de rehabilitación.

- Todo el procesamiento es LOCAL (no se envía a internet).
- Los datos se guardan únicamente si activa --record.
- Puede retirar su consentimiento eliminando ~/.rehab_cv/consent_given

¿Acepta participar? [S/n]: """, end="")
    try:
        resp = input().strip().lower()
    except EOFError:
        return False
    return resp in ("", "s", "si", "sí", "y", "yes")


def require_consent(
    headless: bool = False,
    accept_consent: bool = False,
    use_gui: bool = True,
) -> bool:
    """
    Verifica el consentimiento. Si no existe, lo solicita.

    Args:
        headless: Si True, omite consentimiento (Docker/CI).
        accept_consent: Si True, assume consentimiento ya dado.
        use_gui: Si True y no headless, usar ventana OpenCV; si no, consola.

    Returns:
        True si proceder, False si el usuario rechazó (llamar sys.exit(1)).
    """
    if headless or accept_consent:
        return True
    if consent_already_given():
        return True

    if use_gui:
        try:
            accepted = show_consent_gui()
        except Exception:
            accepted = show_consent_console()
    else:
        accepted = show_consent_console()

    if not accepted:
        log.warning("Consentimiento no otorgado. Finalizando.")
        return False

    save_consent()
    return True
