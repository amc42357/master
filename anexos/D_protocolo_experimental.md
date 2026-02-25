# Anexo D: Protocolo Experimental Operativo

Documento paso a paso para la ejecución de la fase de validación (Cap. 6). Incluye checklist de preparación, guión de instrucciones para participantes, plantilla de hoja de registro y procedimiento de sincronización y backup de datos.

---

## 1. Lista de verificación (*checklist*) de preparación

Completar **antes** de cada sesión de validación.

### 1.1. Equipo

| **Elemento** | **Verificación** |
| :--- | :--- |
| PC con Python 3.9+ | □ Sistema operativo Windows 10/11 o macOS; Python y `venv` instalados. |
| Cámara web | □ Logitech C920 o equivalente; 1080p, 30 FPS; conectada y reconocida. |
| Goniómetro | □ Goniómetro de brazos largos disponible y calibrado. |
| Metrónomo | □ App o dispositivo para 1 repetición cada 3 s (20 BPM aprox.). |
| Hoja de registro | □ Plantilla impresa (sección 3) para el sujeto de la sesión. |

### 1.2. Software

| **Elemento** | **Verificación** |
| :--- | :--- |
| Entorno virtual | □ `venv` activado; dependencias instaladas (`pip install -r requirements.txt`). |
| Prototipo | □ Script principal ejecutable; prueba rápida de captura y detección de pose. |
| Script de análisis | □ Script de análisis (Pandas/Matplotlib) disponible y probado con datos de ejemplo. |

### 1.3. Sala

| **Elemento** | **Verificación** |
| :--- | :--- |
| Iluminación | □ Luz uniforme; sin contraluces fuertes hacia la cámara. |
| Distancia | □ Espacio para colocar al sujeto a **2 m** de la cámara. |
| Evaluador | □ Posición del evaluador con goniómetro sin obstruir la vista de la cámara. |
| Marcas anatómicas | □ Si se usan, acromion (hombro) y epicóndilo lateral (codo) marcados en la piel del sujeto. |

---

## 2. Guión estandarizado de instrucciones para participantes

Leer en voz alta (o adaptar ligeramente) antes de iniciar la sesión.

---

**Presentación:**  
"Buenos días / Buenas tardes. Gracias por participar. Voy a explicarte en qué consiste la sesión."

**Objetivo:**  
"Estamos validando un sistema de visión por computadora que mide el ángulo del hombro y cuenta repeticiones durante un ejercicio de rehabilitación. Tu participación nos ayuda a comprobar que el sistema funciona correctamente."

**Qué haremos:**  
"Te grabaré con la cámara mientras haces elevaciones laterales del brazo —levantar el brazo hacia un lado y bajarlo—. Un compañero medirá el ángulo con un goniómetro en cada repetición. Todo el proceso es local: las imágenes no se envían por internet."

**Duración:**  
"Aproximadamente 20–30 minutos, incluyendo la explicación y tres series de 10 repeticiones con descanso entre series."

**Ejercicio:**  
"Harás 3 series de 10 repeticiones. Un metrónomo marcará el ritmo: una repetición cada 3 segundos. Mantén el brazo recto y sube hasta donde puedas sin forzar, luego baja con control."

**Preguntas:**  
"¿Tienes alguna duda antes de empezar? Si en algún momento quieres parar, lo hacemos sin problema."

---

*Una vez respondidas las dudas, solicitar la firma del consentimiento informado (Anexo A) y proceder con la configuración y calibración según el protocolo (Cap. 6.3).*

---

## 3. Plantilla de hoja de registro en papel

Imprimir una hoja por sujeto. Usar para registrar ángulo goniómetro y validez del conteo humano por repetición.

**ID Sujeto:** _______________   **Fecha:** _______________   **Evaluador:** _______________

| **Serie** | **Rep** | **Ángulo goniómetro (°)** | **Conteo humano (válida)** | **Observaciones** |
| :---: | :---: | :---: | :---: | :--- |
| 1 | 1 | | □ Sí □ No | |
| 1 | 2 | | □ Sí □ No | |
| 1 | 3 | | □ Sí □ No | |
| 1 | 4 | | □ Sí □ No | |
| 1 | 5 | | □ Sí □ No | |
| 1 | 6 | | □ Sí □ No | |
| 1 | 7 | | □ Sí □ No | |
| 1 | 8 | | □ Sí □ No | |
| 1 | 9 | | □ Sí □ No | |
| 1 | 10 | | □ Sí □ No | |
| 2 | 1 | | □ Sí □ No | |
| 2 | 2 | | □ Sí □ No | |
| … | … | | | |
| 3 | 10 | | □ Sí □ No | |

*Rep = Repetición. "Conteo humano (válida)": ciclo completo que supere 60° según el evaluador.*

---

## 4. Procedimiento de sincronización de datos y backup

### 4.1. Sincronización

- Los logs CSV del sistema incluyen **timestamp** (y opcionalmente `frame_id`) por cada *frame* o por cada evento registrado.
- Alinear las **repeticiones** del sistema con las de la hoja de registro usando:
  - el orden temporal de las repeticiones (1.ª, 2.ª, … por serie), y  
  - los timestamps para asociar cada repetición del CSV con la fila correspondiente de la hoja (ángulo goniómetro, válida sí/no).
- En el script de análisis, emparejar cada repetición válida del sistema con la medición de referencia (goniómetro) para calcular el MAE y la precisión de conteo.

### 4.2. Convención de nombres de archivos

- **Logs del sistema:** `Sujeto_X_Serie_Y.csv` (ej. `Sujeto_1_Serie_1.csv`), o `Sujeto_X_sesion.csv` si se registra toda la sesión en un solo CSV.
- **Hojas de registro:** `Sujeto_X_hoja_registro.pdf` (o escaneo) y, si se digitalizan, `Sujeto_X_hoja_registro.csv`.

### 4.3. Estructura de backup

- **Carpeta principal:** `validacion_YYYYMMDD/` (fecha de la sesión o del backup).
  - `datos_crudos/`: logs CSV generados por el prototipo.
  - `hojas_registro/`: copias escaneadas o fotos de las hojas de registro.
  - `analisis/`: copia del script de análisis y de los resultados (gráficos, tablas).
- Realizar **backup** en disco externo o nube institucional tras cada sesión, manteniendo los mismos nombres y estructura para facilitar el análisis posterior.
