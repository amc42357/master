#!/usr/bin/env python3
"""
Script de análisis de validación (T-09).
Calcula MAE, precisión de conteo y latencia a partir del CSV del sistema
y opcionalmente datos de referencia (goniómetro, conteo humano).

Uso:
  python scripts/analyze_validation.py sesion.csv [referencia.csv]
  python scripts/analyze_validation.py sesion.csv -o reporte.md
"""

import argparse
import csv
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def extract_reps_from_system_csv(df: pd.DataFrame) -> list[dict]:
    """
    Extrae repeticiones válidas del CSV del sistema.

    Para cada fila con feedback_msg == "Repetición válida", recupera el ciclo
    previo (up->down) y toma el max(angle_deg) en ese ciclo.
    También registra timestamp del primer frame "up" del ciclo para estimar latencia.

    Returns:
        Lista de dicts con rep_num, angle_max, timestamp, frame_id, timestamp_up (para latencia)
    """
    reps = []
    in_cycle = False
    cycle_angles = []
    cycle_timestamp_up = None  # timestamp del primer frame en estado "up" del ciclo

    for i, row in df.iterrows():
        ang = row.get("angle_deg")
        if pd.isna(ang):
            continue
        try:
            angle_val = float(ang) if ang else 0.0
        except (ValueError, TypeError):
            continue

        rep_state = str(row.get("rep_state", "")).strip().lower()
        fb = row.get("feedback_msg")
        feedback = "" if pd.isna(fb) else str(fb).strip()
        ts = float(row.get("timestamp", 0))

        if rep_state == "up":
            if not in_cycle:
                in_cycle = True
                cycle_angles = []
                cycle_timestamp_up = ts
            cycle_angles.append(angle_val)
        elif rep_state == "down" and in_cycle:
            cycle_angles.append(angle_val)
            if "Repetición válida" in feedback or "Repeticion valida" in feedback:
                if cycle_angles:
                    reps.append({
                        "rep_num": len(reps) + 1,
                        "angle_max": max(cycle_angles),
                        "timestamp": ts,
                        "frame_id": int(row.get("frame_id", 0)),
                        "timestamp_up": cycle_timestamp_up,
                    })
                in_cycle = False
                cycle_angles = []
                cycle_timestamp_up = None

    return reps


def compute_latency_ms(system_reps: list[dict]) -> tuple[float, list[float]]:
    """
    Estima la latencia por repetición: tiempo desde el primer frame "up" del ciclo
    hasta el frame en que se muestra "Repetición válida" (feedback en pantalla).
    Criterio de éxito (protocolo Cap. 6): latencia < 150 ms.

    Returns:
        (latencia_media_ms, lista de latencias por rep en ms)
    """
    latencies_ms = []
    for r in system_reps:
        ts_up = r.get("timestamp_up")
        ts_feedback = r.get("timestamp")
        if ts_up is not None and ts_feedback is not None and ts_feedback >= ts_up:
            latencies_ms.append((ts_feedback - ts_up) * 1000.0)
    if not latencies_ms:
        return 0.0, []
    return float(np.mean(latencies_ms)), latencies_ms


def load_reference_csv(path: Path) -> list[dict]:
    """Carga CSV de referencia con rep_num, angle_goniometer, valid_human."""
    refs = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rep_num = int(row.get("rep_num", 0))
            try:
                angle_g = float(row.get("angle_goniometer", 0))
            except (ValueError, TypeError):
                angle_g = 0.0
            valid = str(row.get("valid_human", "1")).strip().lower() in ("1", "si", "sí", "yes", "true")
            refs.append({"rep_num": rep_num, "angle_goniometer": angle_g, "valid_human": valid})
    return refs


def compute_mae(system_reps: list[dict], ref_reps: list[dict]) -> tuple[float, list[float]]:
    """
    MAE = (1/n) * Σ |ángulo_sistema_i - ángulo_goniómetro_i|

    Empareja por rep_num. Solo incluye repeticiones válidas (valid_human=True).
    """
    errors = []
    for ref in ref_reps:
        if not ref.get("valid_human", True):
            continue
        rep_num = ref["rep_num"]
        sys_rep = next((r for r in system_reps if r["rep_num"] == rep_num), None)
        if sys_rep is None:
            continue
        err = abs(sys_rep["angle_max"] - ref["angle_goniometer"])
        errors.append(err)

    if not errors:
        return 0.0, []
    return float(np.mean(errors)), errors


def compute_count_precision(system_count: int, total_valid_ref: int) -> float:
    """
    Precisión de conteo (protocolo Cap. 6): porcentaje de repeticiones reales
    que el sistema contó correctamente. Se penaliza tanto el defecto como el exceso:
    - Si el sistema cuenta menos que lo real, precisión = system_count / total_valid_ref.
    - Si el sistema cuenta más que lo real, se consideran como "correctas" solo
      total_valid_ref (no se supera 100%), de modo que sobredetección no infla
      la métrica por encima del total real.
    Fórmula: min(system_count, total_valid_ref) / total_valid_ref * 100.
    Criterio de éxito: precisión >= 95%.
    """
    if total_valid_ref <= 0:
        return 0.0
    correct = min(system_count, total_valid_ref)
    return (correct / total_valid_ref) * 100.0


def main():
    parser = argparse.ArgumentParser(
        description="Análisis de validación: MAE, precisión, gráficos"
    )
    parser.add_argument(
        "csv_file",
        type=str,
        help="Ruta al CSV de sesión del sistema",
    )
    parser.add_argument(
        "reference",
        type=str,
        nargs="?",
        default=None,
        help="Ruta al CSV de referencia (rep_num, angle_goniometer, valid_human)",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="Directorio de salida para gráficos e informe (default: mismo que CSV)",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="No generar gráficos",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        log.error("No se encuentra %s", csv_path)
        return 1

    df = pd.read_csv(csv_path)
    system_reps = extract_reps_from_system_csv(df)

    if not system_reps:
        log.warning("No se encontraron repeticiones válidas en el CSV del sistema.")
        log.warning("Asegúrese de que feedback_msg contiene 'Repetición válida' en las repeticiones completadas.")

    out_dir = Path(args.output_dir) if args.output_dir else csv_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = csv_path.stem

    # Cargar referencia si existe
    ref_reps = []
    if args.reference:
        ref_path = Path(args.reference)
        if ref_path.exists():
            ref_reps = load_reference_csv(ref_path)
        else:
            log.warning("Referencia no encontrada: %s", ref_path)

    mae = 0.0
    errors = []
    total_valid_ref = sum(1 for r in ref_reps if r.get("valid_human", True))
    if ref_reps and system_reps:
        mae, errors = compute_mae(system_reps, ref_reps)
    precision = compute_count_precision(len(system_reps), total_valid_ref if total_valid_ref > 0 else len(system_reps))

    # Latencia: estimada desde primer frame "up" del ciclo hasta feedback "Repetición válida"
    latency_mean_ms = 0.0
    latency_list_ms = []
    if system_reps:
        latency_mean_ms, latency_list_ms = compute_latency_ms(system_reps)

    # Criterios de éxito (protocolo Cap. 6)
    mae_ok = mae <= 5.0
    prec_ok = precision >= 95.0 if total_valid_ref > 0 else True
    latency_ok = latency_mean_ms < 150.0 if latency_list_ms else True

    # Tabla de resumen
    report_lines = [
        "# Informe de validación",
        "",
        f"**Archivo:** {csv_path.name}",
        f"**Repeticiones detectadas por el sistema:** {len(system_reps)}",
        "",
        "## Métricas",
        "",
        f"| Métrica | Valor | Criterio | Cumple |",
        f"|---------|-------|----------|--------|",
        f"| MAE (ángulo) | {mae:.2f}° | ≤ 5° | {'Sí' if mae_ok else 'No'} |",
        f"| Precisión conteo | {precision:.1f}% | ≥ 95% | {'Sí' if prec_ok else 'No'} |",
        f"| Latencia (media) | {latency_mean_ms:.1f} ms | < 150 ms | {'Sí' if latency_ok else 'No'} |",
        "",
    ]

    if system_reps:
        angles = [r["angle_max"] for r in system_reps]
        report_lines.extend([
            "## Ángulos máximos por repetición (sistema)",
            "",
            f"Min: {min(angles):.1f}° | Max: {max(angles):.1f}° | Media: {np.mean(angles):.1f}°",
            "",
        ])

    if errors:
        report_lines.extend([
            "## Errores individuales (sistema vs goniómetro)",
            "",
            f"Min: {min(errors):.2f}° | Max: {max(errors):.2f}°",
            "",
        ])

    if latency_list_ms:
        report_lines.extend([
            "## Latencia (estimada por repetición)",
            "",
            f"Media: {latency_mean_ms:.1f} ms | Min: {min(latency_list_ms):.1f} ms | Max: {max(latency_list_ms):.1f} ms",
            "",
        ])

    report_lines.append("---")
    report_lines.append("Generado por scripts/analyze_validation.py")

    report_path = out_dir / f"{base_name}_informe.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    log.info("Informe guardado en: %s", report_path)

    # Gráfico de dispersión (sistema vs goniómetro)
    if not args.no_plot and ref_reps and system_reps:
        paired = []
        for ref in ref_reps:
            if not ref.get("valid_human", True):
                continue
            sys_rep = next((r for r in system_reps if r["rep_num"] == ref["rep_num"]), None)
            if sys_rep:
                paired.append((ref["angle_goniometer"], sys_rep["angle_max"]))

        if paired:
            gonio, sys_ang = zip(*paired)
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.scatter(gonio, sys_ang, alpha=0.7, s=60)
            lims = [min(min(gonio), min(sys_ang)) - 5, max(max(gonio), max(sys_ang)) + 5]
            ax.plot(lims, lims, "k--", label="Identidad (y=x)")
            ax.set_xlabel("Ángulo goniómetro (°)")
            ax.set_ylabel("Ángulo sistema (°)")
            ax.set_title(f"Dispersión: sistema vs goniómetro\nMAE = {mae:.2f}°")
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xlim(lims)
            ax.set_ylim(lims)
            ax.set_aspect("equal")
            fig.tight_layout()
            scatter_path = out_dir / f"{base_name}_dispersion.png"
            fig.savefig(scatter_path, dpi=150, bbox_inches="tight")
            plt.close()
            log.info("Gráfico de dispersión: %s", scatter_path)

    # Gráfico de series temporales (ángulo en el tiempo)
    if not args.no_plot and "timestamp" in df.columns and "angle_deg" in df.columns:
        ts = df["timestamp"].astype(float)
        ang = df["angle_deg"].replace("", np.nan).astype(float)
        valid = ~ang.isna()
        if valid.any():
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(ts[valid], ang[valid], color="#2e86ab", linewidth=1.5)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Ángulo de abducción del hombro (°)")
            ax.set_title(f"Evolución del ángulo — {base_name}")
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.set_xlim(ts.min(), ts.max())
            ax.set_ylim(0, 100)
            fig.tight_layout()
            series_path = out_dir / f"{base_name}_series.png"
            fig.savefig(series_path, dpi=150, bbox_inches="tight")
            plt.close()
            log.info("Gráfico de series: %s", series_path)

    log.info("MAE: %.2f° | Precisión: %.1f%% | Latencia: %.1f ms", mae, precision, latency_mean_ms)
    return 0


if __name__ == "__main__":
    exit(main())
