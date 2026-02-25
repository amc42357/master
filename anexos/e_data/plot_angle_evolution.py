#!/usr/bin/env python3
"""
Genera un gráfico de evolución del ángulo de abducción del hombro en el tiempo
a partir del log CSV de una sesión. Ejemplo de salida del módulo de análisis
(Anexo E del proyecto).
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

def main():
    base = Path(__file__).resolve().parent
    csv_path = base / "session_sample.csv"
    out_path = base / "angle_evolution_example.png"

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]
    timestamps = [float(r["timestamp"]) for r in rows]
    angles = [float(r["angle_deg"]) for r in rows]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timestamps, angles, color="#2e86ab", linewidth=1.5)
    ax.set_xlabel("Tiempo (s)", fontsize=11)
    ax.set_ylabel("Ángulo de abducción del hombro (°)", fontsize=11)
    ax.set_title("Evolución del ángulo en el tiempo — Sesión de ejemplo (anonimizada)")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xlim(min(timestamps), max(timestamps))
    ax.set_ylim(0, 100)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Gráfico guardado en: {out_path}")

if __name__ == "__main__":
    main()
