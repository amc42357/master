# Anexo B: Backlog Completo del Producto y Planificación de Sprints

Este anexo expande la Tabla 4 del Capítulo 4. Se incluyen todas las historias de usuario (US) y tareas técnicas (T) con identificación única, descripción, criterios de aceptación, puntos de historia, sprint planificado y sprint en que se completaron.

---

## Tabla del Backlog Completo

| **ID** | **Tipo** | **Historia / Tarea** | **Descripción breve** | **Criterios de aceptación** | **Puntos** | **Sprint planificado** | **Sprint completado** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **US-01** | US | Configuración del Entorno | **Como** desarrollador, **quiero** un entorno Python con OpenCV y MediaPipe **para** empezar el desarrollo. | (1) `venv` creado; (2) `requirements.txt` con opencv-python, mediapipe, numpy; (3) script de prueba que importa las librerías sin error; (4) proyecto en Git con estructura base `/src`, `/docs`, `/data`. | 1 | Sprint 1 | Sprint 1 |
| **US-02** | US | Captura de Video en Tiempo Real | **Como** usuario, **quiero** que el sistema muestre el video de mi cámara web **para** verificar que me detecta. | (1) Captura con OpenCV desde cámara por defecto; (2) ventana que muestra el video en vivo; (3) cierre correcto al pulsar tecla; (4) resolución 720p o superior configurable. | 2 | Sprint 2 | Sprint 2 |
| **US-03** | US | Visualización del Esqueleto Corporal | **Como** usuario, **quiero** ver los puntos clave (hombro, codo, cadera) superpuestos **para** confirmar la detección. | (1) MediaPipe Pose integrado (`pose_landmarker_full`); (2) dibujo de *landmarks* y conexiones sobre el *frame*; (3) al menos hombro, codo y cadera visibles y estables; (4) integrado con la ventana de video de US-02. | 3 | Sprint 3 | Sprint 3 |
| **US-04** | US | Cálculo y Visualización de Ángulo | **Como** usuario, **quiero** ver en tiempo real el ángulo de elevación del brazo **para** conocer mi rango de movimiento. | (1) Cálculo del ángulo de abducción (cadera–hombro–codo) con geometría vectorial; (2) valor numérico en grados visible en pantalla; (3) actualización *frame* a *frame*; (4) código documentado y con pruebas básicas. | 5 | Sprint 4 | Sprint 4 |
| **US-05** | US | Conteo Automático de Repeticiones | **Como** usuario, **quiero** que el sistema cuente cada elevación lateral válida **para** saber cuántas llevo. | (1) Máquina de estados que detecta ciclos subida/bajada; (2) umbrales angulares configurables (ej. 60° para repetición válida); (3) contador visible en pantalla que se actualiza al completar una repetición; (4) sin falsos positivos/negativos evidentes en pruebas internas. | 5 | Sprint 5 | Sprint 5 |
| **US-06** | US | Retroalimentación de Corrección | **Como** usuario, **quiero** mensajes claros cuando mi movimiento sea incorrecto **para** corregirlo al momento. | (1) Mensajes de texto según reglas (ej. "Levante más el brazo", "Repetición válida"); (2) criterios basados en umbrales de ángulo y estado; (3) mensajes visibles en zona dedicada de la GUI; (4) integración con el módulo de conteo (US-05). | 8 | Sprint 6 | Sprint 6 |
| **T-07** | T | Diseño del Protocolo de Validación | **Como** investigador, **quiero** el protocolo experimental con *baseline* (goniómetro) **para** validar el sistema. | (1) Documento con hipótesis, métricas (MAE, precisión, latencia) y criterios de éxito; (2) fases: reclutamiento, configuración, ejecución, análisis; (3) materiales: consentimiento (Anexo A), hoja de registro, guión; (4) revisión y aprobación del equipo. | 3 | Sprint 7 | Sprint 7 |
| **T-08** | T | Pruebas de Validación y Recolección de Datos | **Como** investigador, **quiero** ejecutar el protocolo con sujetos **para** obtener métricas. | (1) Al menos 5 sujetos sanos reclutados; (2) consentimiento firmado; (3) 3×10 repeticiones por sujeto con goniómetro y grabación; (4) logs CSV del sistema y hojas de registro completas; (5) backup de datos en carpeta definida. | 8 | Sprint 8 | Sprint 11–12 |
| **T-09** | T | Análisis de Datos y Generación de Gráficos | **Como** investigador, **quiero** analizar datos y crear gráficas **para** evaluar criterios de éxito. | (1) Script Python (Pandas/SciPy) que calcula MAE, precisión y latencia; (2) gráficos de dispersión (ángulo sistema vs. goniómetro) y series temporales; (3) tablas de resumen por sujeto y global; (4) informe breve con resultados y limitaciones. | 5 | Sprint 9 | Sprint 13–14 |
| **US-10** | US | Exportación de Reportes | **Como** usuario/terapeuta, **quiero** exportar CSV/PDF con sesión (repeticiones, ángulos) **para** llevar registro. | (1) Exportación a CSV con timestamp, ángulo, estado de repetición, etc.; (2) opción de exportar a PDF o resumen legible si hay tiempo; (3) archivos guardados en carpeta local elegida por el usuario; (4) documentado en README. | 5 | Sprint 10 | Sprint 10 (si hay tiempo) |

---

## Resumen por Sprint

| **Sprint** | **Ítems completados** | **Puntos** |
| :--- | :--- | :--- |
| Sprint 1 | US-01 | 1 |
| Sprint 2 | US-02 | 2 |
| Sprint 3 | US-03 | 3 |
| Sprint 4 | US-04 | 5 |
| Sprint 5 | US-05 | 5 |
| Sprint 6 | US-06 | 8 |
| Sprint 7 | T-07 | 3 |
| Sprint 8 | — | 0 |
| Sprint 9 | — | 0 |
| Sprint 10 | US-10 (opcional) | 5 |
| Sprint 11–12 | T-08 | 8 |
| Sprint 13–14 | T-09 | 5 |

*Nota:* T-08 y T-09 se planifican en Sprints 8 y 9 pero se ejecutan en Sprints 11–12 y 13–14 según el cronograma detallado (Cap. 5.1), que reserva las últimas semanas a validación experimental, análisis y documentación.
