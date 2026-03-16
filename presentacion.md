---
marp: true
theme: default
title: Rehabilitación motriz asistida por visión por computadora
description: Trabajo de innovación - Seminario IA - UNIR
paginate: true
---

<!-- _class: lead -->
# Rehabilitación motriz asistida por visión por computadora

**Trabajo de innovación**  
Seminario de Innovación en IA

**Equipo:** Cesar Francisco Sandoval González, Adelaid Lesdemyariet Acevedo Cardona, Armando Morales Carmona, José Rolando Ríos Cisneros

Universidad Internacional de La Rioja (UNIR) · ESIT · Maestría en Inteligencia Artificial  
Madrid, 27 de febrero de 2026

---

# Índice

1. Contexto y motivación
2. Planteamiento del problema
3. Objetivos
4. Desarrollo conceptual (Design Thinking)
5. Metodología: Scrum y Lean — 5b. Gestión: Jira
6. Implementación y arquitectura
7. Validación y diseño experimental
8. Conclusiones y trabajo futuro

---

# 1. Contexto y motivación

- **ACV:** una de las principales causas de discapacidad motora a nivel mundial; hasta un 80 % de supervivientes con hemiparesia/hemiplejía (Langhorne et al., 2011).
- **Rehabilitación tradicional:** barreras de acceso (coste, disponibilidad, geografía); la pandemia acentuó la necesidad de telerrehabilitación (Laver et al., 2020).
- **IA en salud:** monitorización objetiva, personalización y extensión del cuidado más allá del entorno clínico (Esteva et al., 2019).
- **Oportunidad:** combinar visión por computadora e IA de código abierto para supervisión objetiva en domicilio con hardware de consumo.

---

# 2. Planteamiento del problema

- **Brecha:** necesidad de rehabilitación motriz intensiva post-ACV vs. acceso limitado a supervisión continua y asequible.
- **Pacientes en domicilio:** sin retroalimentación objetiva en tiempo real → riesgo de ejecución incorrecta, baja adherencia, recuperación subóptima.
- **Soluciones actuales** (Kinect, sensores, robótica): barreras de costo y complejidad; poca adopción domiciliaria.
- **Necesidad:** solución accesible, bajo costo y fácil de usar con hardware convencional (p. ej. cámara web) que supervisie, evalúe y guíe ejercicios de forma autónoma.

---

# 3. Objetivos

**Objetivo general**  
Desarrollar un prototipo de software basado en CV y aprendizaje automático que asista la ejecución domiciliaria de ejercicios de rehabilitación de hombro para pacientes post-ACV y valide su precisión frente a goniómetro y conteo humano (**MAE ≤ 5°**, **precisión ≥ 95 %**).

**Objetivos específicos (resumen)**  
1. Módulo de estimación de pose 2D (MediaPipe, 33 landmarks).  
2. Algoritmos de análisis cinemático (ángulo abducción, máquina de estados, conteo).  
3. Interfaz y retroalimentación (video + esqueleto + ángulo + contador + mensajes).  
4. Validación (MAE, precisión, informe comparativo).  
5. Documentación y repositorio (README, requirements.txt, informe de validación).

---

# 4. Desarrollo conceptual (Design Thinking)

- **Empatizar:** paciente (dolor: acceso limitado, desmotivación; ganancia: autonomía, guía) y terapeuta (dolor: imposibilidad de supervisar; ganancia: datos objetivos).
- **Definir:** reto HMW — herramienta accesible (cámara web) con supervisión y retroalimentación objetiva comparable a guía del terapeuta.
- **Idear:** Idea A (móvil), Idea B (web/nube), **Idea C (escritorio, local)**.
- **Prototipar y seleccionar:** Idea C elegida (matriz MELDS: mejor en privacidad, accesibilidad y viabilidad; puntuación 9,15).

---

# 5. Metodología: Scrum y Lean

- **Scrum:** Product Owner, Scrum Master, equipo de desarrollo; backlog priorizado, sprints de 1 semana, 16 semanas; DoR/DoD definidos.
- **Lean:** Idear → Construir → Medir → Aprender → Decidir; velocidad = puntos de historia completados por sprint; bug rate, valor de negocio.
- **Backlog:** US-01 a US-06 (entorno, captura, esqueleto, ángulo, conteo, retroalimentación), T-07 a T-09 (protocolo, pruebas, análisis), US-10 (exportación); Fibonacci 1–8.
- **Repositorio:** github.com/amc42357/master

---

# 5b. Gestión del proyecto: Jira

- Seguimiento del backlog y de los sprints en **Jira** (instancia local con Docker).
- Uso de **épicas** (E1: Prototipo core, E2: Validación experimental, E3: Entrega), **historias de usuario** (US-01 a US-10) y **tareas** (T-07 a T-09).
- Backlog alineado con el documento del proyecto; criterios de aceptación y story points volcados en Jira.
- Capturas de evidencia (backlog, board de sprint, detalle de épica y story) en el documento y en el Anexo G.

---

# 6. Implementación y arquitectura

- **Arquitectura:** modular monolítica en Python; modelo **C4** (contexto: paciente, sistema, cámara; contenedores: captura OpenCV → pose MediaPipe → cálculo NumPy → lógica → GUI → CSV).
- **Stack:** Python 3.9+, OpenCV, MediaPipe Pose, NumPy, Pandas, Matplotlib/Seaborn; datos en CSV locales, sin video crudo; procesamiento 100 % local (privacidad).
- **Plazo:** 16 semanas (12 desarrollo, 4 validación y documentación); coste directo cero (software libre).
- **Entorno:** Windows/macOS/Linux; mensaje de consentimiento al iniciar; SemVer, ramas y PRs.

---

# 7. Validación y diseño experimental

- **Hipótesis:** H1) MAE ≤ 5° vs. goniómetro; H2) precisión ≥ 95 % en conteo vs. evaluador humano; H3) latencia &lt; 150 ms (criterio).
- **Métricas:** MAE angular, precisión de conteo, latencia, robustez (≥ 3 condiciones de luz).
- **Protocolo:** 5 sujetos sanos, consentimiento informado, 3×10 repeticiones abducción hombro, goniómetro + log CSV; análisis con Pandas/SciPy.
- **Normativa y ética:** Ley 14/2007 (investigación biomédica), Ley 41/2002 (autonomía paciente), RGPD/LOPDGDD, Reglamento IA (UE) 2024/1689 (riesgo limitado).

---

# 8. Conclusiones y trabajo futuro

**Conclusiones**  
- Sistema de asistencia para rehabilitación motriz domiciliaria post-ACV basado en CV, centrado en accesibilidad, viabilidad y privacidad.  
- Design Thinking + Scrum/Lean permiten un MVP acotado en 16 semanas con criterios verificables (MAE ≤ 5°, precisión ≥ 95 %).

**Limitaciones**  
Validación con sujetos sanos; un ejercicio (hombro); entorno controlado.

**Trabajo futuro**  
Piloto con pacientes post-ACV; más ejercicios (codo, rodilla, tobillo); personalización; integración FHIR; robustez con transfer learning.

---

<!-- _class: lead -->
# Gracias

**Rehabilitación motriz asistida por visión por computadora**

Repositorio: **github.com/amc42357/master**

UNIR · Maestría en Inteligencia Artificial · 2026
