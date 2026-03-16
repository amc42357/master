"""
Módulo de interfaz gráfica (US-06) con Dear PyGui o fallback OpenCV.
Ventana de video + métricas (progress bar, textos). Use REHAB_USE_DPG=1 para DPG.
"""

import os
from typing import Optional

import numpy as np

try:
    import dearpygui.dearpygui as dpg
    _DPG_AVAILABLE = True
except ImportError:
    _DPG_AVAILABLE = False
    dpg = None

# Usar DPG solo si está instalado y el usuario lo pide (evita segfaults en algunos entornos)
HAS_DPG = _DPG_AVAILABLE and os.environ.get("REHAB_USE_DPG", "").strip().lower() in ("1", "true", "yes")

from . import config

TARGET_ANGLE = config.ANGLE_THRESHOLD_VALID_REP
# Límite superior de la escala visual (grados)
RULER_ANGLE_MAX = 90.0
# Umbral "bajar hasta" para la guía
THRESHOLD_DOWN_DEG = config.ANGLE_THRESHOLD_DOWN

# Estado para salida con tecla
_exit_requested = False
_texture_tag = "rehab_texture"
_widget_ids: dict = {}


def _feedback_text(
    feedback_msg: str,
    angle_deg: Optional[float],
    rep_state: str,
) -> str:
    """Misma lógica que antes: texto a mostrar según feedback, ángulo y estado."""
    if feedback_msg:
        return feedback_msg
    if angle_deg is None:
        return "Colocate frente a la camara con hombro y brazo visibles"
    if rep_state == "up":
        return "Muy bien. Ahora baja el brazo con control para completar la repeticion"
    if angle_deg < TARGET_ANGLE:
        falta = TARGET_ANGLE - angle_deg
        if falta > 25:
            return f"Sube el brazo hacia un lado. Falta unos {int(falta)} para el objetivo ({int(TARGET_ANGLE)})"
        return f"Casi. Sube un poco mas (objetivo {int(TARGET_ANGLE)})"
    return "Sube el brazo hasta 60 o mas para contar una repeticion valida"


def frame_bgr_to_texture_data(frame: np.ndarray) -> np.ndarray:
    """Convierte frame BGR (OpenCV) a array 1D float RGB normalizado para DPG."""
    data = np.flip(frame, 2)  # BGR -> RGB
    data = data.ravel()
    data = np.asarray(data, dtype=np.float32)
    return data / 255.0


def setup_dpg(width: int, height: int) -> None:
    """Crea contexto DPG, viewport, textura y ventanas de video y métricas."""
    global _exit_requested, _widget_ids
    _exit_requested = False

    dpg.create_context()
    dpg.create_viewport(
        title="Rehabilitación - Abducción de hombro",
        width=min(width + 360, 1600),
        height=min(height + 80, 900),
    )
    dpg.setup_dearpygui()

    # Textura para el frame (video + esqueleto)
    placeholder = np.zeros((height * width * 3), dtype=np.float32)
    with dpg.texture_registry():
        dpg.add_raw_texture(
            width,
            height,
            placeholder,
            tag=_texture_tag,
            format=dpg.mvFormat_Float_rgb,
        )

    # Ventana de video
    with dpg.window(label="Video", tag="win_video", no_title_bar=False):
        dpg.add_image(_texture_tag)

    # Ventana de métricas
    num_series = getattr(config, "NUM_SERIES", 3)
    reps_per_series = getattr(config, "REPS_PER_SERIES", 10)
    with dpg.window(label="Métricas", tag="win_metrics", pos=(width + 20, 20)):
        dpg.add_text("Abducción de hombro", tag="txt_title")
        dpg.add_text(
            f"Objetivo: {num_series} series × {reps_per_series} rep — Ritmo: 1 rep cada 3 s (metrónomo)",
            tag="txt_protocol",
            color=(180, 220, 180),
        )
        dpg.add_separator()
        _widget_ids["angle"] = dpg.add_text("Ángulo: ---", tag="txt_angle")
        dpg.add_progress_bar(default_value=0.0, tag="prog_angle", show=True)
        dpg.add_text("Objetivo: 60°", tag="txt_target")
        _widget_ids["state"] = dpg.add_text("Estado: BAJAR", tag="txt_state")
        _widget_ids["count"] = dpg.add_text("Repeticiones: 0", tag="txt_count")
        _widget_ids["series"] = dpg.add_text(
            f"Serie 1 de {num_series} — Rep 0 de {reps_per_series}",
            tag="txt_series",
        )
        _widget_ids["recording"] = dpg.add_text("", tag="txt_recording")
        dpg.add_separator()
        _widget_ids["feedback"] = dpg.add_text("", tag="txt_feedback", wrap=400)
        dpg.add_separator()
        dpg.add_text("Q o ESC = Salir", color=(150, 150, 150))

    def _on_key(sender, app_data, user_data):
        if app_data in (81, 256):  # Q or ESC
            global _exit_requested
            _exit_requested = True

    with dpg.handler_registry():
        dpg.add_key_press_handler(callback=_on_key)

    dpg.show_viewport()


def update_texture(frame_bgr: np.ndarray) -> None:
    """Actualiza la textura con el frame (BGR, numpy)."""
    data = frame_bgr_to_texture_data(frame_bgr)
    dpg.set_value(_texture_tag, data)


def update_ui(
    angle_deg: Optional[float],
    rep_count: int,
    rep_state: str,
    feedback_msg: str,
    is_recording: bool,
    current_series: int = 1,
    rep_in_series: int = 0,
) -> None:
    """Actualiza progress bar y textos según estado actual."""
    # Progress bar: 0..1 hacia objetivo 60°
    if angle_deg is not None:
        progress = min(1.0, max(0.0, angle_deg / TARGET_ANGLE))
    else:
        progress = 0.0
    dpg.set_value("prog_angle", progress)

    num_series = getattr(config, "NUM_SERIES", 3)
    reps_per_series = getattr(config, "REPS_PER_SERIES", 10)

    angle_str = f"{angle_deg:.1f}" if angle_deg is not None else "---"
    dpg.set_value("txt_angle", f"Ángulo: {angle_str}°")
    dpg.set_value("txt_state", "Estado: SUBIR" if rep_state == "up" else "Estado: BAJAR")
    dpg.set_value("txt_count", f"Repeticiones: {rep_count}")
    dpg.set_value(
        "txt_series",
        f"Serie {current_series} de {num_series} — Rep {rep_in_series} de {reps_per_series}",
    )
    dpg.set_value("txt_recording", "GRABANDO" if is_recording else "")
    text = _feedback_text(feedback_msg, angle_deg, rep_state)
    dpg.set_value("txt_feedback", text)


def is_running() -> bool:
    """True si DPG sigue activo y el usuario no ha pedido salir."""
    global _exit_requested
    return dpg.is_dearpygui_running() and not _exit_requested


def render_frame_dpg() -> None:
    """Renderiza un frame de la UI DPG."""
    dpg.render_dearpygui_frame()


def cleanup_dpg() -> None:
    """Destruye el contexto DPG."""
    dpg.destroy_context()


def render_frame(
    frame: np.ndarray,
    frame_with_skeleton: np.ndarray,
    angle_deg: Optional[float],
    rep_count: int,
    feedback_msg: str,
    rep_state: str = "down",
    is_recording: bool = False,
    current_series: int = 1,
    rep_in_series: int = 0,
) -> np.ndarray:
    """
    Con DPG: devuelve frame con esqueleto (overlay en ventana DPG).
    Sin DPG: dibuja overlay con OpenCV y devuelve frame compuesto.
    """
    if HAS_DPG:
        return frame_with_skeleton
    return _render_frame_opencv(
        frame_with_skeleton,
        angle_deg,
        rep_count,
        feedback_msg,
        rep_state,
        is_recording,
        current_series,
        rep_in_series,
    )


def _draw_angle_ruler(out: np.ndarray, angle_deg: Optional[float], h: int, w: int) -> None:
    """Dibuja una escala vertical de referencia (0°–90°) a la derecha y el ángulo actual."""
    import cv2
    rx1, rx2 = w - 72, w - 24
    ry1, ry2 = 160, h - 100
    ruler_h = ry2 - ry1
    # Fondo de la regla
    cv2.rectangle(out, (rx1 - 4, ry1), (rx2 + 4, ry2), (35, 35, 40), -1)
    cv2.rectangle(out, (rx1 - 4, ry1), (rx2 + 4, ry2), (100, 100, 110), 2)
    # Ticks: 0 abajo, 90 arriba
    for deg in (0, 30, 45, 60, 90):
        t = 1.0 - (deg / RULER_ANGLE_MAX)
        py = int(ry1 + t * ruler_h)
        cv2.line(out, (rx2, py), (rx2 + 6, py), (180, 180, 180), 1)
        cv2.putText(out, f"{deg}", (rx1 - 28, py + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    # Zona objetivo 60° (banda verde)
    t60 = 1.0 - (TARGET_ANGLE / RULER_ANGLE_MAX)
    t45 = 1.0 - (THRESHOLD_DOWN_DEG / RULER_ANGLE_MAX)
    py60 = int(ry1 + t60 * ruler_h)
    py45 = int(ry1 + t45 * ruler_h)
    cv2.rectangle(out, (rx1, py60), (rx2, ry2), (0, 80, 0), -1)
    cv2.rectangle(out, (rx1, py45), (rx2, py60), (0, 60, 80), -1)
    # Indicador del ángulo actual
    if angle_deg is not None:
        t_cur = 1.0 - (min(RULER_ANGLE_MAX, max(0, angle_deg)) / RULER_ANGLE_MAX)
        pcur = int(ry1 + t_cur * ruler_h)
        cv2.line(out, (rx1, pcur), (rx2 + 4, pcur), (0, 255, 200), 3)
        cv2.circle(out, (rx2 + 2, pcur), 5, (0, 255, 200), -1)
    cv2.putText(out, "Angulo", (rx1 - 2, ry1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)


# --- Fallback OpenCV cuando DPG no está instalado ---
def _render_frame_opencv(
    frame: np.ndarray,
    angle_deg: Optional[float],
    rep_count: int,
    feedback_msg: str,
    rep_state: str,
    is_recording: bool,
    current_series: int = 1,
    rep_in_series: int = 0,
) -> np.ndarray:
    """Dibujo manual con cv2 (panel, barra, regla de referencia, feedback). Trabaja en una copia para evitar parpadeo."""
    import cv2
    num_series = getattr(config, "NUM_SERIES", 3)
    reps_per_series = getattr(config, "REPS_PER_SERIES", 10)
    # Trabajar siempre sobre una copia; evita parpadeo al no modificar el buffer en uso por imshow
    out = np.ascontiguousarray(frame.copy())
    h, w = out.shape[:2]
    # Panel métricas (más alto para serie/rep e instrucción)
    x, y, pw, ph = 16, 16, 320, 200
    overlay = out.copy()
    cv2.rectangle(overlay, (x, y), (x + pw, y + ph), (45, 45, 50), -1)
    out = cv2.addWeighted(overlay, 0.85, out, 0.15, 0)
    cv2.rectangle(out, (x, y), (x + pw, y + ph), (120, 120, 120), 2)
    # Objetivo del protocolo
    cv2.putText(
        out,
        f"Objetivo: {num_series} series x {reps_per_series} rep (1 rep/3s)",
        (x + 12, y + 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (180, 220, 180),
        1,
    )
    cv2.putText(out, "Angulo: " + (f"{angle_deg:.1f}" if angle_deg is not None else "---"),
                (x + 12, y + 48), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    progress = min(1.0, max(0.0, (angle_deg or 0) / TARGET_ANGLE))
    fill_w = int((pw - 24) * progress)
    cv2.rectangle(out, (x + 12, y + 58), (x + 12 + (pw - 24), y + 82), (50, 50, 55), -1)
    # Color de la barra según zona: verde objetivo, amarillo subiendo, gris bajo
    if angle_deg is not None:
        if angle_deg >= TARGET_ANGLE:
            bar_color = (0, 200, 0)
        elif angle_deg >= THRESHOLD_DOWN_DEG:
            bar_color = (0, 200, 255)
        else:
            bar_color = (80, 80, 120)
    else:
        bar_color = (80, 80, 120)
    if fill_w > 0:
        cv2.rectangle(out, (x + 12, y + 58), (x + 12 + fill_w, y + 82), bar_color, -1)
    cv2.putText(out, "SUBIR" if rep_state == "up" else "BAJAR",
                (x + pw - 70, y + 48), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
    # Serie y repetición en la serie (destacado)
    cv2.putText(
        out,
        f"Serie {current_series} de {num_series}",
        (x + 12, y + 108),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 200),
        2,
    )
    cv2.putText(
        out,
        f"Repeticion {rep_in_series} de {reps_per_series}",
        (x + 12, y + 132),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (255, 255, 0),
        2,
    )
    cv2.putText(out, f"Total: {rep_count}", (x + 12, y + 158), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    if is_recording:
        cv2.putText(out, "GRABANDO", (x + pw - 92, y + 26), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
    # Regla de referencia (baseline visual)
    _draw_angle_ruler(out, angle_deg, h, w)
    # Guía de movimiento (baseline de cómo hacer el ejercicio)
    guide_y = h - 148
    cv2.rectangle(out, (16, guide_y), (w - 88, guide_y + 52), (40, 42, 50), -1)
    cv2.rectangle(out, (16, guide_y), (w - 88, guide_y + 52), (90, 90, 100), 1)
    cv2.putText(out, "3 series de 10 rep. Ritmo: 1 rep cada 3 s (metronomo).", (24, guide_y + 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 220, 180), 1)
    cv2.putText(out, "Sube el brazo hasta la zona verde (60), bajalo con control.", (24, guide_y + 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 220, 180), 1)
    # Feedback durante el movimiento
    text = _feedback_text(feedback_msg, angle_deg, rep_state)
    bar_h, bar_y = 64, h - 80
    cv2.rectangle(out, (16, bar_y), (w - 88, bar_y + bar_h), (40, 40, 45), -1)
    cv2.rectangle(out, (16, bar_y), (w - 88, bar_y + bar_h), (120, 120, 120), 2)
    # Indicador de "lo estás haciendo bien": color según estado
    if angle_deg is not None and rep_state == "up" and angle_deg >= TARGET_ANGLE:
        status_color = (0, 255, 100)
        status_short = "Objetivo alcanzado - Baja con control"
    elif feedback_msg:
        status_color = (255, 220, 100)
        status_short = text
    else:
        status_color = (255, 255, 255)
        status_short = text
    cv2.putText(out, (status_short or text)[:70], (24, bar_y + 36), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
    cv2.putText(out, "Q o ESC = Salir", (w - 220, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
    return out
