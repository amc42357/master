#!/usr/bin/env python3
"""Genera un video de prueba para verificar el pipeline sin cámara."""

import cv2
import numpy as np
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent.parent
    out_path = base / "data" / "test_video.mp4"
    (base / "data").mkdir(exist_ok=True)

    w, h, fps = 640, 480, 30
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, fps, (w, h))

    for i in range(fps * 3):  # 3 segundos
        frame = np.ones((h, w, 3), dtype=np.uint8) * ((i % 2) * 30 + 80)
        writer.write(frame)

    writer.release()
    print(f"Video creado: {out_path}")

if __name__ == "__main__":
    main()
