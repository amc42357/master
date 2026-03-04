#!/usr/bin/env python3
"""
Genera un gráfico de evolución del ángulo de abducción del hombro en el tiempo
a partir del log CSV de una sesión. Usado en la fase de validación (T-09).
"""

import argparse
import csv
import logging
from pathlib import Path

import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Grafica evolución del ángulo desde CSV de sesión"
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default=None,
        help="Ruta al CSV de sesión (default: data/session_sample.csv)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Ruta de salida del gráfico PNG",
    )
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    data_dir = base / "data"

    if args.csv_file:
        csv_path = Path(args.csv_file)
    else:
        csv_path = data_dir / "session_sample.csv"

    if not csv_path.exists():
        log.error("No se encuentra %s", csv_path)
        log.info("Use: python scripts/plot_angle_evolution.py ruta/sesion.csv")
        return 1

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = csv_path.with_suffix(".png")

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]

    timestamps = []
    angles = []
    for r in rows:
        try:
            ts = float(r["timestamp"])
            ang = r.get("angle_deg", "")
            ang_val = float(ang) if ang else 0.0
            timestamps.append(ts)
            angles.append(ang_val)
        except (ValueError, KeyError):
            continue

    if not timestamps:
        log.error("No hay datos válidos en el CSV")
        return 1

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timestamps, angles, color="#2e86ab", linewidth=1.5)
    ax.set_xlabel("Tiempo (s)", fontsize=11)
    ax.set_ylabel("Ángulo de abducción del hombro (°)", fontsize=11)
    ax.set_title("Evolución del ángulo en el tiempo — Sesión (anonimizada)")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xlim(min(timestamps), max(timestamps))
    ax.set_ylim(0, 100)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    log.info("Gráfico guardado en: %s", out_path)
    return 0


if __name__ == "__main__":
    exit(main())
