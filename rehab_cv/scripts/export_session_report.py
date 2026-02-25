#!/usr/bin/env python3
"""
Script de exportación de reporte de sesión a PDF (US-10).
Genera un resumen legible con repeticiones, ángulos máximos y estadísticas.

Uso:
  python scripts/export_session_report.py data/sesion.csv [-o reporte.pdf]
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# fpdf2 es opcional; usarlo solo si está instalado
try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False


def extract_reps(df: pd.DataFrame) -> list[dict]:
    """Extrae repeticiones válidas del CSV del sistema."""
    reps = []
    in_cycle = False
    cycle_angles = []

    for _, row in df.iterrows():
        ang = row.get("angle_deg")
        if pd.isna(ang):
            continue
        try:
            angle_val = float(ang)
        except (ValueError, TypeError):
            continue

        rep_state = str(row.get("rep_state", "")).strip().lower()
        fb = row.get("feedback_msg")
        feedback = "" if pd.isna(fb) else str(fb).strip()

        if rep_state == "up":
            if not in_cycle:
                in_cycle = True
                cycle_angles = []
            cycle_angles.append(angle_val)
        elif rep_state == "down" and in_cycle:
            cycle_angles.append(angle_val)
            if "Repetición válida" in feedback or "Repeticion valida" in feedback:
                if cycle_angles:
                    reps.append({
                        "rep_num": len(reps) + 1,
                        "angle_max": max(cycle_angles),
                        "timestamp": float(row.get("timestamp", 0)),
                    })
                in_cycle = False
                cycle_angles = []

    return reps


def generate_pdf(reps: list[dict], csv_name: str, output_path: Path) -> None:
    """Genera PDF con resumen de la sesión."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=16)
    newline = {"new_x": "LMARGIN", "new_y": "NEXT"}
    pdf.cell(0, 10, "Reporte de sesion - Rehabilitacion motriz", **newline)
    pdf.set_font("helvetica", size=10)
    pdf.cell(0, 6, f"Archivo: {csv_name}", **newline)
    pdf.ln(5)

    pdf.set_font("helvetica", size=12, style="B")
    pdf.cell(0, 8, "Resumen", **newline)
    pdf.set_font("helvetica", size=10)
    pdf.cell(0, 6, f"Repeticiones completadas: {len(reps)}", **newline)

    if reps:
        angles = [r["angle_max"] for r in reps]
        avg_angle = sum(angles) / len(angles)
        min_angle = min(angles)
        max_angle = max(angles)
        pdf.cell(0, 6, f"Angulo medio: {avg_angle:.1f} grados", **newline)
        pdf.cell(0, 6, f"Angulo min/max: {min_angle:.1f} / {max_angle:.1f} grados", **newline)
        pdf.ln(5)

        pdf.set_font("helvetica", size=11, style="B")
        pdf.cell(0, 6, "Angulo maximo por repeticion", **newline)
        pdf.set_font("helvetica", size=10)
        for r in reps:
            pdf.cell(0, 5, f"  Rep {r['rep_num']}: {r['angle_max']:.1f} grados (t={r['timestamp']:.1f}s)", **newline)

    pdf.ln(10)
    pdf.set_font("helvetica", size=8)
    pdf.cell(0, 5, "Sistema de rehabilitacion motriz - Vision por computadora (UNIR)", **newline)
    pdf.cell(0, 5, "Generado por scripts/export_session_report.py", **newline)

    pdf.output(str(output_path))


def main():
    parser = argparse.ArgumentParser(
        description="Exporta resumen de sesion a PDF"
    )
    parser.add_argument(
        "csv_file",
        type=str,
        help="Ruta al CSV de sesion",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Ruta de salida del PDF (default: mismo nombre con .pdf)",
    )
    args = parser.parse_args()

    if not HAS_FPDF:
        print("Error: Se requiere fpdf2. Instale con: pip install fpdf2", file=sys.stderr)
        return 1

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: No se encuentra {csv_path}", file=sys.stderr)
        return 1

    df = pd.read_csv(csv_path)
    reps = extract_reps(df)

    out_path = Path(args.output) if args.output else csv_path.with_suffix(".pdf")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    generate_pdf(reps, csv_path.name, out_path)
    print(f"Reporte PDF guardado en: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
