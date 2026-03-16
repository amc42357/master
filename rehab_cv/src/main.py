#!/usr/bin/env python3
"""
Punto de entrada del sistema de rehabilitación motriz.
Bucle principal: capture -> pose -> angle -> rep_counter -> gui -> (opcional CSV).
"""

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

import cv2

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
log = logging.getLogger(__name__)

# Añadir el directorio raíz al path para imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.capture import VideoCapture
from src.consent import require_consent
from src.pose_detector import PoseDetector
from src.angle_calculator import calculate_shoulder_abduction_angle
from src.rep_counter import RepCounter
from src.gui import (
    HAS_DPG,
    render_frame,
    setup_dpg,
    update_texture,
    update_ui,
    render_frame_dpg,
    is_running,
    cleanup_dpg,
)
from src.session_logger import SessionLogger
from src import config


def parse_args():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Sistema de rehabilitación motriz - Visión por computadora"
    )
    parser.add_argument(
        "--video",
        type=str,
        default=None,
        help="Ruta a archivo de video para pruebas (sin cámara)",
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Índice de la cámara (default: 0)",
    )
    parser.add_argument(
        "--record",
        action="store_true",
        help="Activar registro de sesión en CSV",
    )
    parser.add_argument(
        "--arm",
        type=str,
        choices=["left", "right"],
        default=config.DEFAULT_ARM,
        help="Brazo a analizar (default: right)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Modo sin ventana (para Docker/CI; procesa hasta fin del video)",
    )
    parser.add_argument(
        "--accept-consent",
        action="store_true",
        help="Asumir consentimiento informado (para CI/scripts no interactivos)",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["lite", "full"],
        default="lite",
        help="Modelo de pose: lite (default, más rápido) o full (más preciso)",
    )
    parser.add_argument(
        "--no-metronome",
        action="store_true",
        help="Desactivar metrónomo (1 rep cada 3 s)",
    )
    return parser.parse_args()


def _play_metronome_beep() -> None:
    """Reproduce un beep corto (cross-platform). No bloquea el bucle principal."""
    try:
        if sys.platform == "darwin":
            subprocess.Popen(
                ["afplay", "/System/Library/Sounds/Tink.aiff"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        elif sys.platform == "win32":
            import winsound
            winsound.Beep(880, 150)
    except Exception:
        pass


def _series_and_rep(rep_count: int, num_series: int, reps_per_series: int) -> tuple[int, int]:
    """Calcula serie actual (1..num_series) y repetición en la serie (0..reps_per_series)."""
    current_series = min(num_series, 1 + (rep_count // reps_per_series))
    rep_in_series = rep_count - (current_series - 1) * reps_per_series
    return current_series, rep_in_series


def main():
    """Bucle principal del sistema."""
    args = parse_args()

    if not require_consent(
        headless=args.headless,
        accept_consent=args.accept_consent,
        use_gui=not args.headless,
    ):
        sys.exit(1)

    source = args.video if args.video else args.camera

    try:
        cap = VideoCapture(
            source=source,
            width=config.CAMERA_WIDTH,
            height=config.CAMERA_HEIGHT,
            fps=config.CAMERA_FPS,
        )
    except RuntimeError as e:
        log.error("%s", e)
        log.info("Sugerencia: use --video ruta/video.mp4 para probar con archivo.")
        sys.exit(1)

    model_path = config.POSE_MODEL_FULL_PATH if args.model == "full" else config.POSE_MODEL_PATH
    pose_detector = PoseDetector(model_path=model_path)
    rep_counter = RepCounter()
    session_logger = SessionLogger()

    if args.record:
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        log_path = session_logger.start()
        log.info("Registrando sesión en: %s", log_path)

    log.info("Mostrando video. Pulse 'q' o ESC para salir.")
    log.info("Resolución: %s x %s", cap.width, cap.height)
    if not args.record:
        log.info("NOTA: Para guardar la sesión use --record")

    use_dpg = not args.headless and HAS_DPG
    if not args.headless and not HAS_DPG:
        cv2.namedWindow("Rehabilitación - Abducción de hombro", cv2.WINDOW_NORMAL)
    if use_dpg:
        setup_dpg(cap.width, cap.height)

    use_metronome = not args.headless and not args.no_metronome
    if use_metronome:
        log.info("Metrónomo activo: 1 rep cada %.1f s", config.METRONOME_INTERVAL_SEC)

    last_beep_time: float | None = None

    try:
        for frame in cap.frames():
            # Metrónomo: beep cada METRONOME_INTERVAL_SEC (1 rep cada 3 s)
            if use_metronome:
                now = time.monotonic()
                if last_beep_time is None:
                    last_beep_time = now
                elif now - last_beep_time >= config.METRONOME_INTERVAL_SEC:
                    _play_metronome_beep()
                    last_beep_time = now

            # Detección de pose
            landmarks = pose_detector.process(frame)
            frame_with_skeleton = pose_detector.draw_landmarks(frame, landmarks)

            # Coordenadas y ángulo
            coords = pose_detector.get_landmark_coords(landmarks, arm=args.arm)
            angle_deg = calculate_shoulder_abduction_angle(coords)

            # Actualizar contador de repeticiones
            state, count, feedback_msg = rep_counter.update(angle_deg)
            current_series, rep_in_series = _series_and_rep(
                count, config.NUM_SERIES, config.REPS_PER_SERIES
            )

            # Registrar en CSV si está activo
            if args.record:
                session_logger.log(
                    coords=coords,
                    angle_deg=angle_deg,
                    rep_state=state.value,
                    feedback_msg=feedback_msg,
                )

            if not args.headless:
                if use_dpg:
                    update_texture(frame_with_skeleton)
                    update_ui(
                        angle_deg,
                        count,
                        state.value,
                        feedback_msg,
                        args.record,
                        current_series=current_series,
                        rep_in_series=rep_in_series,
                    )
                    render_frame_dpg()
                    if not is_running():
                        break
                else:
                    display = render_frame(
                        frame,
                        frame_with_skeleton,
                        angle_deg,
                        count,
                        feedback_msg,
                        rep_state=state.value,
                        is_recording=args.record,
                        current_series=current_series,
                        rep_in_series=rep_in_series,
                    )
                    cv2.imshow("Rehabilitación - Abducción de hombro", display)
                    key = cv2.waitKey(max(1, int(1000 / 30))) & 0xFF
                    if key == ord("q") or key == 27:
                        break

    finally:
        cap.release()
        pose_detector.close()
        if args.record:
            session_logger.stop()
            log.info("Sesión guardada en: %s", config.DATA_DIR)
        if use_dpg:
            cleanup_dpg()
        else:
            cv2.destroyAllWindows()

    log.info("Sesión finalizada.")


if __name__ == "__main__":
    main()
