# Protocolo de validación – Sujeto 1

**Fecha:** 2026-03-03 (sesión 18:53)  
**Sujeto:** 1 (primer sujeto de prueba)

## Antes de empezar

- [x] Cámara web colocada estable, a ~2 m de ti.
- [ ] Iluminación uniforme (evitar contraluz).
- [ ] Fondo neutro y despejado.
- [x] Brazo a analizar: **derecho** (por defecto; si usas el izquierdo: `--arm left`).

## Ejercicio

**Abducción de hombro:** elevación lateral del brazo en el plano frontal (levantar el brazo hacia un lado, como alzando la mano en clase).

- **Ritmo:** ~1 repetición cada 3 segundos (puedes usar un metrónomo en 20 BPM o contar mentalmente "sube-pausa-baja-pausa").
- **Repetición válida:** el sistema cuenta cuando superas el umbral (p. ej. 60°). Sube hasta donde puedas cómodamente (90° o más si quieres) y baja con control.

## Sesión (3 series × 10 repeticiones)

**Archivo de sesión:** `sesion_20260303_185303.csv`  
**Datos del sistema (capturados):** 1491 frames · duración 101,7 s · repeticiones contadas por el sistema: **31** · ángulo máx. registrado: **129,9°** · ángulo mín.: 4,3°

| Serie | Repeticiones | Ángulo máx. goniómetro (opcional) | Notas |
|-------|--------------|-----------------------------------|-------|
| 1     | 10           | —                                 |       |
| 2     | 10           | —                                 |       |
| 3     | 10           | —                                 |       |

*(Sin medición con goniómetro en esta sesión; el sistema registró ángulos en el CSV.)*

## Comando para grabar la sesión

Desde la raíz del proyecto `rehab_cv`:

```bash
source venv/bin/activate   # Windows: venv\Scripts\activate
python src/main.py --record
```

1. Si es la primera vez, **acepta el consentimiento** (tecla **S**).
2. Colócate frente a la cámara; verás el esqueleto y el ángulo en pantalla.
3. Haz **3 series de 10 repeticiones** con pausas breves entre series.
4. Al terminar, pulsa **q** o **ESC** para cerrar y guardar.

El CSV se guardará en `data/sesion_YYYYMMDD_HHMMSS.csv`.

## Después

- Revisar el CSV en `data/`.
- Opcional: generar gráfico con  
  `python scripts/plot_angle_evolution.py data/sesion_YYYYMMDD_HHMMSS.csv -o grafico.png`
- Si tienes referencia con goniómetro:  
  `python scripts/analyze_validation.py data/sesion_*.csv referencia.csv -o data`
