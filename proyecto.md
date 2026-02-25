---
# Formato UNIR (basado en plantilla del seminario)
title: "PROPUESTA DE TRABAJO DE INNOVACIÓN: SISTEMA DE VISIÓN POR COMPUTADORA PARA REHABILITACIÓN MOTRIZ POST-EVENTO CEREBROVASCULAR"
subtitle: "MAESTRÍA EN INTELIGENCIA ARTIFICIAL - UNIVERSIDAD INTERNACIONAL DE LA RIOJA (UNIR)"
lang: es
documentclass: article
papersize: a4
geometry:
  - left=3cm
  - right=2cm
  - top=2.5cm
  - bottom=2.5cm
fontsize: 12pt
linestretch: 1.5
mainfont: "Helvetica"
---

## **ÍNDICE**

1. Introducción  
2. Objetivos  
3. Desarrollo conceptual (Design Thinking)  
4. Metodología: Scrum y Lean  
5. Implementación de la propuesta  
6. Validación y diseño experimental  
7. Conclusiones y trabajo futuro  
8. Referencias  
9. Anexos  

\newpage

## **1. INTRODUCCIÓN**

### **1.1. Contexto y Motivación**
El accidente cerebrovascular (ACV) constituye una de las principales causas de discapacidad motora adquirida a nivel mundial, con una incidencia que genera una carga significativa para los sistemas de salud y la calidad de vida de los individuos y sus familias (Organización Mundial de la Salud [OMS], 2017). En México, es la quinta causa de muerte y la primera de discapacidad en adultos, situación que se refleja en diversas entidades federativas del país (Instituto Nacional de Estadística y Geografía [INEGI], 2021). Tras un ACV, hasta un 80% de los supervivientes presenta hemiparesia o hemiplejía, requiriendo procesos prolongados de rehabilitación motriz para recuperar funcionalidad en las extremidades superiores, siendo la movilidad del hombro fundamental para las actividades de la vida diaria (Langhorne et al., 2011).

La rehabilitación tradicional, basada en terapia presencial y repetitiva, enfrenta barreras críticas de acceso, incluyendo la limitada disponibilidad de especialistas, los altos costos asociados y las dificultades geográficas para asistencia continua. Esta situación se agravó durante y después de la pandemia por COVID-19, y mostró la necesidad urgente de modelos complementarios de tele-rehabilitación efectivos y escalables (Laver et al., 2020). En este contexto, la Inteligencia Artificial (IA) emerge como un catalizador para la innovación en salud, ofreciendo herramientas para monitorización objetiva, personalización de terapias y extensión del cuidado más allá del entorno clínico (Esteva et al., 2019).

### **1.2. Planteamiento del Problema**
Existe una brecha crítica entre la necesidad de rehabilitación motriz intensiva y repetitiva post-ACV y la capacidad del sistema de salud para proporcionar un acceso continuo, supervisado y asequible a dichos servicios. Los pacientes que realizan ejercicios en domicilio carecen de retroalimentación objetiva en tiempo real sobre la calidad de su movimiento, lo que puede conducir a una ejecución incorrecta, compensaciones musculares indeseadas, baja adherencia al tratamiento y, en última instancia, una recuperación funcional subóptima.

Si bien existen soluciones tecnológicas en el mercado (como sistemas basados en Kinect, sensores inerciales o robótica), estas suelen presentar barreras de costo, complejidad técnica o necesidad de hardware especializado, limitando su adopción masiva en el ámbito domiciliario. Por lo tanto, se identifica la necesidad de una solución accesible, de bajo costo y fácil de usar que, empleando hardware convencional, permita supervisar, evaluar y guiar ejercicios de rehabilitación de forma autónoma.

### **1.3. Justificación e Innovación**
Esta propuesta se justifica por su potencial para generar un impacto tangible en un problema de salud pública, alineándose con los Objetivos de Desarrollo Sostenible (ODS), particularmente con el ODS 3 (Salud y Bienestar). La innovación no radica en la creación de un nuevo algoritmo de estimación de pose, sino en la aplicación integrada, simplificada y centrada en el usuario de tecnologías de visión por computadora (CV) e IA de código abierto para resolver un problema clínico específico.

El valor agregado de la propuesta reside en su viabilidad y accesibilidad: utiliza una cámara web estándar y librerías de software libre (OpenCV, MediaPipe), eliminando la dependencia de hardware costoso. Su novedad está en el diseño de un sistema integral que, partiendo de la detección de pose, automatiza la evaluación cuantitativa (ángulos, repeticiones) y proporciona retroalimentación correctiva inmediata, emulando funciones clave del terapeuta y empoderando al paciente en su proceso de recuperación domiciliaria.

### **1.4. Alcance**
El proyecto se desarrollará en un plazo de 16 semanas, dentro del marco del Seminario de Innovación en IA de UNIR. El alcance del **Producto Mínimo Viable (MVP)** se delimita específicamente a:
*   **Población:** Personas con secuelas motoras en miembro superior tras un ACV (simulada inicialmente con sujetos sanos para pruebas de concepto).
*   **Ejercicio:** Abducción/aducción de hombro en el plano frontal (elevación lateral del brazo), por ser un movimiento fundamental y evaluable.
*   **Tecnología:** Visión por computadora 2D, sin uso de sensores de profundidad o hardware adicional.
*   **Objetivo:** Validar la precisión técnica del sistema en medición angular y conteo, no la efectividad clínica a largo plazo (lo cual requeriría un estudio posterior).

El éxito de la validación se medirá mediante criterios explícitos y verificables: **Error Absoluto Medio (MAE) ≤ 5°** en la medición angular frente a goniómetro como referente estándar, y **precisión ≥ 95%** en el conteo de repeticiones respecto al conteo realizado por un evaluador humano. Estos indicadores, vinculados directamente al alcance del MVP, permiten una evaluación objetiva del prototipo.

### **1.5. Estructura del Documento**
Este documento se estructura en nueve capítulos, siguiendo una lógica que construye la solución desde la definición de fines hasta la validación empírica. Tras esta introducción, el Capítulo 2 define los objetivos generales y específicos; el 3 presenta el desarrollo conceptual (*Design Thinking*), anclando las decisiones en las necesidades del usuario y el estado del arte; el 4 detalla la metodología (*Scrum* y *Lean Startup*) que guiará la ejecución; el 5 describe la implementación técnica; el 6 especifica el diseño experimental y la validación; el 7 recoge conclusiones y líneas de trabajo futuro. Cierran el documento las Referencias y los Anexos. El orden responde a una secuencia: qué se busca (objetivos), por qué y para quién (conceptual), cómo se ejecutará (metodología e implementación) y cómo se demostrará el logro (validación). Los criterios de éxito ya fijados (MAE ≤ 5°, precisión ≥ 95%) se validarán de forma explícita en el Capítulo 6 mediante el protocolo experimental.

\newpage

## **2. OBJETIVOS**

### **2.1. Objetivo General**
Desarrollar un prototipo de software basado en visión por computadora y aprendizaje automático que asista la ejecución domiciliaria de ejercicios de rehabilitación de hombro para pacientes post-ACV, mediante captura con cámara convencional, cálculo de métricas objetivas (ángulo articular y conteo de repeticiones) y retroalimentación visual en tiempo real, validando su precisión frente a goniómetro y conteo humano (MAE ≤ 5°, precisión ≥ 95%), con el propósito de ofrecer una herramienta accesible, de bajo costo y trazable que complemente la terapia tradicional.

### **2.2. Objetivos Específicos**
Para lograr el objetivo general, se establecen los siguientes objetivos específicos, redactados como acciones medibles y verificables. Cada uno concluye con la evidencia esperada que permitirá confirmar su cumplimiento:

1.  **Implementar un módulo de estimación de pose humana en 2D** que detecte de forma estable las coordenadas de 33 puntos anatómicos clave (hombro, codo, cadera y torácicos) desde el flujo de video de una cámara web, utilizando la librería MediaPipe Pose. *Evidencia:* módulo funcional integrado que procesa video en tiempo real y entrega coordenadas normalizadas de los *landmarks*.

2.  **Desarrollar algoritmos de análisis cinemático** que calculen en tiempo real el ángulo de abducción del hombro (geometría vectorial cadera–hombro–codo) e identifiquen ciclos de movimiento mediante una máquina de estados con umbrales configurables. *Evidencia:* funciones probadas que devuelven ángulo en grados y estado del ciclo (subida/bajada) por *frame*.

3.  **Integrar un sistema de interfaz y retroalimentación** que muestre video en vivo con esqueleto superpuesto, ángulo actual, contador de repeticiones y mensajes correctivos según umbrales. *Evidencia:* ventana gráfica operativa con los cuatro elementos integrados y mensajes de guía visibles.

4.  **Validar el rendimiento del prototipo** comparando las métricas del sistema (ángulo máximo por repetición, conteo) contra el goniómetro y el conteo humano, cuantificando MAE y precisión porcentual. *Evidencia:* informe con valores de MAE y precisión obtenidos, tabla comparativa y conclusiones sobre el cumplimiento de los criterios (MAE ≤ 5°, precisión ≥ 95%).

5.  **Documentar el proceso, el código y los resultados** con manual de uso, justificación de decisiones de diseño, código fuente comentado en repositorio Git e informe de validación. *Evidencia:* repositorio con README, requirements.txt y documentación actualizada; informe de validación con resultados y limitaciones.

\newpage

## **3. DESARROLLO CONCEPTUAL (DESIGN THINKING)**

El capítulo aplica *Design Thinking* en seis etapas para definir la solución, anclada en las necesidades del usuario, el estado del arte y la viabilidad técnica.

### **3.1. Empatizar**
La etapa de empatía se centró en comprender en profundidad las experiencias, frustraciones y aspiraciones de los dos usuarios principales: el **paciente post-ACV** y el **terapeuta rehabilitador**.

**Método y análisis:** Se realizó un análisis documental estructurado con los siguientes criterios: (a) búsqueda en bases académicas (PubMed, IEEE Xplore, Scopus) con términos clave *stroke rehabilitation*, *telerehabilitation*, *computer vision*, *pose estimation*, período 2014–2024; (b) revisión de guías clínicas (OMS, Langhorne et al., Laver et al.) sobre rehabilitación post-ACV y tele-rehabilitación; (c) categorización de necesidades en *pains* (dolores) y *gains* (ganancias) según perfiles de usuario; (d) triangulación de hallazgos entre literatura clínica y reportes de tecnologías existentes (Debnath et al., 2021; Saposnik et al., 2016). A partir de este proceso se identificaron los siguientes hallazgos clave (Tabla 1):

*   **Para el Paciente:**
    *   **Dolor:** Acceso limitado y costoso a terapia presencial continua, especialmente en zonas remotas o con recursos limitados. Desmotivación y falta de adherencia debido a la monotonía de los ejercicios y a la ausencia de retroalimentación inmediata sobre su progreso. Incertidumbre sobre si los ejercicios domiciliarios se realizan correctamente.
    *   **Ganancia:** Autonomía para ejercitarse en casa. Recibir guía y confirmación de que el movimiento es correcto. Visualizar el progreso de manera tangible para mantenerse motivado. Un sistema accesible que no requiera una inversión económica alta.

*   **Para el Terapeuta:**
    *   **Dolor:** Imposibilidad de supervisar de forma objetiva y continua la rehabilitación domiciliaria. Carga administrativa alta para el seguimiento manual del progreso. Dificultad para cuantificar con precisión métricas como el rango de movimiento o el número de repeticiones efectivas. Estudios recientes indican que tecnologías como la realidad virtual pueden aumentar la adherencia del paciente, aunque no siempre se traducen en mejoras clínicas significativas superiores a la terapia convencional, destacando la necesidad de herramientas complementarias efectivas y objetivas (Saposnik et al., 2016).
    *   **Ganancia:** Disponer de datos objetivos y automatizados del desempeño del paciente en casa. Poder ajustar el tratamiento basado en evidencia cuantitativa. Optimizar el tiempo de consulta presencial al tener un historial claro del trabajo realizado en domicilio.

*Tabla 1. Resumen de hallazgos de la etapa Empatizar.*
| **Usuario** | **Dolor** | **Ganancia** |
| :--- | :--- | :--- |
| **Paciente post-ACV** | Acceso limitado a terapia; desmotivación y baja adherencia; incertidumbre sobre la corrección del ejercicio domiciliario. | Autonomía en casa; guía y confirmación del movimiento; progreso tangible; sistema accesible y de bajo costo. |
| **Terapeuta** | Imposibilidad de supervisar y cuantificar el trabajo domiciliario; carga administrativa. | Datos objetivos automatizados; ajuste del tratamiento con evidencia; optimización del tiempo de consulta. |

Esta comprensión estableció la base humana del proyecto: la necesidad de un puente tecnológico confiable entre la clínica y el hogar.

**Trazabilidad narrativa:** Los hallazgos de la Tabla 1 derivaron directamente en el reto HMW (Definir); los criterios de éxito se alinearon con las ganancias identificadas (accesibilidad, precisión, retroalimentación, trazabilidad); la selección del prototipo (Idea C) se sustentó en estos criterios mediante la matriz ponderada. De este modo, el flujo hallazgos → reto → criterios → decisiones del MVP queda explícitamente trazado.

### **3.2. Definir (HMW + Criterios de Éxito)**
Sintetizando los hallazgos de la empatía, se formuló el siguiente reto de diseño, estructurado como una pregunta "How Might We?" (¿Cómo podríamos?):

**"¿Cómo podríamos proporcionar a los pacientes post-ACV una herramienta de rehabilitación motriz domiciliaria que sea tan accesible como una cámara web, pero que ofrezca una supervisión y retroalimentación objetiva comparable a la guía inicial de un terapeuta, para mejorar la confianza, la adherencia y la calidad del ejercicio?"**

A partir de este reto, se derivaron los **Criterios de Éxito** iniciales para la solución:
1.  **Accesibilidad Económica:** Costo de implementación cercano a cero para el usuario final (hardware de consumo estándar).
2.  **Precisión Técnica:** Capacidad de medir ángulos articulares con un error aceptable frente a instrumentos estándar (goniómetro).
3.  **Retroalimentación en Tiempo Real:** Generación de guías visuales o auditivas inmediatas durante la ejecución del ejercicio.
4.  **Usabilidad:** Interfaz intuitiva que no requiera capacitación extensa.
5.  **Trazabilidad:** Registro automático de métricas (repeticiones, ángulos máximos) para seguimiento del progreso.

### **3.3. Investigación de Antecedentes (Estado del Arte)**
Se revisaron las soluciones existentes en rehabilitación asistida por tecnología (Debnath et al., 2021). La Tabla 2 compara distintas aproximaciones según integración con el paciente y aplicabilidad clínica, apoyada en la literatura (Basteris et al., 2014; Debnath et al., 2021; Saposnik et al., 2016).

*Tabla 2. Análisis comparativo del estado del arte en rehabilitación asistida.*
| **Categoría / Ejemplo** | **Descripción** | **Ventajas** | **Desventajas / Limitaciones** | **Posicionamiento de la Propuesta** |
| :--- | :--- | :--- | :--- | :--- |
| **Terapia Manual Convencional** | Supervisión presencial por un fisioterapeuta. | Estándar de oro, evaluación integral, interacción humana. | Coste elevado, acceso limitado, métricas subjetivas o manuales. | Busca **complementar** la terapia, extendiendo su alcance al domicilio con métricas objetivas. |
| **Dispositivos Robóticos y Exoesqueléticos** | Sistemas que asisten o guían el movimiento (ej. Armeo Power, InMotion ARM; Basteris et al., 2014). | Alta precisión, asistencia física, intensidad repetitiva sostenida. | **Costo prohibitivo**, tamaño, complejidad, confinados a clínicas especializadas. | Propone una alternativa **no robótica** y de **bajo costo**, eliminando la principal barrera de acceso. |
| **Sistemas de Realidad Virtual (VR)** | Entornos inmersivos para rehabilitación (ej. Oculus Quest con software VITALIS; Saposnik et al., 2016). | Alta motivación y adherencia, entornos seguros para practicar. | **Costo moderado-alto**, no siempre muestra superioridad clínica significativa frente a terapia convencional, equipo especializado. | Se enfoca en la **precisión de medición y corrección** del movimiento real, no en la inmersión lúdica. |
| **Plataformas de Software Clínico** | Software para gestión y prescripción de ejercicios (ej. SPRY, WebPT). | Excelentes para gestión clínica, planes de tratamiento. | Se centran en la **administración**, no en la **evaluación automatizada** del movimiento en tiempo real. Carecen de *feedback* objetivo durante la ejecución. | Aporta el componente de **análisis automático de movimiento** que estas plataformas no suelen incluir, pudiendo ser un módulo complementario. |
| **Aplicaciones Móviles Instructivas** | Apps con videos y recordatorios para ejercicios. | Muy accesibles, bajo costo, promueven la adherencia. | **Carecen de retroalimentación objetiva**. El paciente puede ejercitarse incorrectamente sin saberlo. | Añade el componente clave de **análisis y retroalimentación automatizada** en tiempo real, garantizando calidad. |

**Conclusión del Análisis:** Hay una brecha entre soluciones de alta tecnología (robótica, VR), costosas y complejas, y otras muy accesibles (apps, videos) pero sin supervisión inteligente. La propuesta apunta a ese hueco: una "supervisión inteligente accesible" que permita análisis automático del movimiento con hardware estándar.

### **3.4. Idear**
En esta etapa se generaron múltiples alternativas para abordar el reto de diseño, evaluando distintas combinaciones de tecnología y entrega.

*   **Idea A - Teléfono Inteligente como Sensor y Pantalla:** Desarrollar una app móvil que use la cámara del teléfono para capturar el movimiento y muestre la retroalimentación en la misma pantalla.
*   **Idea B - Sistema Web con Procesamiento en la Nube:** Crear una aplicación web donde el usuario se conecte vía *streaming* de video; el procesamiento de visión por computadora se realizaría en un servidor remoto.
*   **Idea C - Software de Escritorio con Procesamiento Local (PROPUESTA ACTUAL):** Desarrollar una aplicación para computadora personal (Windows/macOS/Linux) que utilice una cámara web externa y procese toda la información localmente en el dispositivo del usuario.

### **3.5. Prototipar**
Se seleccionó la **Idea C** para prototipar. El **Producto Mínimo Viable (MVP)** será un script en Python ejecutable, con una interfaz gráfica simple, que cumpla con el flujo core:
1.  **Entrada:** Captura de video en tiempo real desde una cámara web USB estándar (720p o superior).
2.  **Procesamiento:** Pipeline que utiliza **OpenCV** para el manejo de video y **MediaPipe Pose** (modelo `pose_landmarker_lite` por defecto; opcionalmente `pose_landmarker_full` con mayor precisión) para la estimación de 33 puntos anatómicos clave en 2D.
3.  **Lógica:** Cálculo del ángulo de abducción del hombro en tiempo real usando geometría vectorial (con los *landmarks* de cadera, hombro y codo). Detección de repeticiones mediante una máquina de estados que identifica ciclos de movimiento (subida/bajada) al cruzar umbrales angulares predefinidos.
4.  **Salida:** Ventana que muestra: a) Video con el esqueleto superpuesto, b) Valor numérico del ángulo, c) Contador de repeticiones, d) Mensajes de texto (ej., "Extienda más el brazo", "Repetición válida") basados en reglas de umbral.

La interfaz se estructura en tres zonas: (1) área central de video con superposición del esqueleto; (2) panel de métricas en la esquina superior (ángulo y contador); (3) barra inferior de mensajes de retroalimentación. Los bocetos de baja fidelidad (*wireframes*) detallados se incluyen en el Anexo C.

**Justificación:** El prototipo prioriza la privacidad (procesamiento local, sin envío de video a la nube), la viabilidad técnica (librerías maduras y documentadas) y la fidelidad al concepto: medición y retroalimentación automatizada con hardware mínimo.

### **3.6. Selección de Prototipo**
Para justificar formalmente la elección de la Idea C, se utilizó una matriz de selección ponderada con criterios alineados a los objetivos del proyecto y al marco MELDS (Tabla 3).

*Tabla 3. Matriz de selección y evaluación de ideas.*
| **Criterio** | **Peso** | **Idea A: App Móvil** | **Idea B: Sistema Web/Cloud** | **Idea C: Software Escritorio (Seleccionada)** |
| :--- | :--- | :--- | :--- | :--- |
| **Viabilidad Técnica (Skills)** | 25% | **Alta (8)**. Depende de compatibilidad entre OS móviles. | **Media-Baja (4)**. Complejidad de infraestructura de *streaming* y procesamiento en servidor. | **Alta (9)**. Python, OpenCV y MediaPipe son tecnologías estables y bien documentadas. |
| **Costo/Accesibilidad (Mindset)** | 25% | **Alta (9)**. Hardware ya poseído por el usuario. | **Media (6)**. Requiere conexión a internet robusta; costos de servidor a escala. | **Muy Alta (10)**. Solo requiere cámara web (ya común) y una PC estándar. |
| **Precisión y Control (Experimentation)** | 20% | **Media (6)**. Posible inestabilidad por movimiento del teléfono. | **Media-Alta (7)**. Depende de la latencia de red y calidad de *streaming*. | **Alta (9)**. Procesamiento local minimiza latencia; cámara fija mejora estabilidad. |
| **Privacidad y Ética (Data)** | 20% | **Alta (8)**. Procesamiento en dispositivo posible. | **Baja (3)**. Video del paciente se transmite y procesa externamente. | **Muy Alta (10)**. **Todo el procesamiento es local.** No hay transmisión de datos biométricos. |
| **Potencial de Integración** | 10% | **Media (5)**. Puede integrarse con *wearables*. | **Alta (8)**. Fácil integración con historiales clínicos en la nube. | **Media-Alta (7)**. Puede exportar datos a formatos estándar (CSV) para su uso posterior. |
| **PUNTAJE TOTAL (Ponderado)** | **100%** | **7.45** | **5.45** | **9.15** |

**Justificación de la Selección:** La Idea C (Software de Escritorio) obtuvo la puntuación más alta, sobre todo en privacidad, accesibilidad y viabilidad técnica, criterios centrales para el MVP en 16 semanas. Resuelve el problema central (supervisión automatizada accesible) de la manera más directa y con menor riesgo técnico, alineándose plenamente con los principios MELDS. La decisión final, por tanto, es proceder con el desarrollo de este prototipo.

\newpage

## **4. METODOLOGÍA: SCRUM Y LEAN**

Este capítulo detalla el marco de trabajo ágil y la filosofía de desarrollo que se adoptarán para gestionar y ejecutar el proyecto. La combinación de **Scrum** y **Lean Startup** proporciona una estructura para organizar el trabajo en equipo, priorizar el valor, gestionar la incertidumbre y asegurar que el desarrollo del prototipo se mantenga enfocado, iterativo y basado en evidencia.

### **4.1. Roles, Artefactos y Eventos**
El proyecto adopta el marco **Scrum** con responsabilidades claras, entregables concretos y reuniones cíclicas que favorecen la transparencia, la inspección y la adaptación continua.

*   **Roles:**
    *   **Product Owner:** Cesar Francisco Sandoval González. Responsable de maximizar el valor del producto y gestionar el *Backlog*, priorizando las funcionalidades según su impacto en el usuario final.
    *   **Scrum Master:** Adelaid Lesdemyariet Acevedo Cardona. Facilita el proceso Scrum, elimina impedimentos y asegura que el equipo comprenda y siga la metodología.
    *   **Equipo de Desarrollo:** Armando Morales Carmona y José Rolando Ríos Cisneros. Responsables colectivos de analizar, diseñar, desarrollar, probar y documentar el incremento del producto en cada Sprint. Ambos aportarán habilidades complementarias en programación Python, visión por computadora (OpenCV) y lógica de aplicación.

*   **Artefactos:**
    *   **Product Backlog:** Lista priorizada y dinámica de todo lo que el producto necesita, desde funcionalidades de alto nivel hasta tareas técnicas específicas. Es responsabilidad del Product Owner.
    *   **Sprint Backlog:** Subconjunto del *Product Backlog* seleccionado para un Sprint, junto con un plan para entregar el Incremento. Es propiedad del Equipo de Desarrollo.
    *   **Incremento:** La suma de todos los elementos del *Product Backlog* completados durante un Sprint y todos los Sprints anteriores. Representa una versión del producto que es potencialmente entregable y funcional.

*   **Eventos (Ceremonias):**
    *   **Sprint Planning (Planificación del Sprint):** Al inicio de cada Sprint (semanal). El equipo selecciona elementos del *Product Backlog* y define el objetivo del Sprint y el plan de trabajo.
    *   **Daily Stand-up (Reunión Diaria):** Breve reunión de 15 minutos donde cada miembro del equipo sincroniza actividades: qué hizo ayer, qué hará hoy y qué impedimentos tiene.
    *   **Sprint Review (Revisión del Sprint):** Al final del Sprint. El equipo presenta el Incremento terminado al Product Owner y otros interesados para recibir *feedback*.
    *   **Sprint Retrospective (Retrospectiva del Sprint):** Tras la revisión. El equipo reflexiona sobre su forma de trabajar para identificar mejoras de proceso para el siguiente Sprint.

### **4.2. Backlog Inicial, Estimación y Cadencia**
El **Backlog Inicial** reúne historias de usuario (*User Stories*) y tareas técnicas, estimadas con puntos de historia por complejidad relativa (escala de Fibonacci: 1, 2, 3, 5, 8). Los **Sprints** serán de una semana, alineados con el cronograma académico de 16 semanas. La priorización se justifica por valor de usuario (primero capacidades core: captura, detección, ángulo, conteo, feedback) y por riesgo técnico (validación y análisis en fases posteriores). Los criterios de aceptación son verificables y permiten un incremento observable por sprint; el detalle completo se documenta en el Anexo B. El backlog priorizado se resume en la Tabla 4.

*Tabla 4. Backlog inicial del producto (priorizado) con criterios de aceptación.*
| **ID** | **Historia de Usuario / Tarea** | **Como.../Para...** | **Estimación** | **Sprint Objetivo** |
| :--- | :--- | :--- | :--- | :--- |
| **US-01** | Configuración del Entorno | **Como** desarrollador, **quiero** un entorno Python configurado con OpenCV y MediaPipe, **para** comenzar el desarrollo de inmediato. | 1 | Sprint 1 |
| **US-02** | Captura de Video en Tiempo Real | **Como** usuario, **quiero** que el sistema inicie y muestre el video de mi cámara web, **para** asegurarme de que me está viendo. | 2 | Sprint 2 |
| **US-03** | Visualización del Esqueleto Corporal | **Como** usuario, **quiero** ver mi propio cuerpo con los puntos clave (hombro, codo, cadera) superpuestos en la pantalla, **para** confirmar que el sistema me detecta correctamente. | 3 | Sprint 3 |
| **US-04** | Cálculo y Visualización de Ángulo | **Como** usuario, **quiero** ver un número que muestre en tiempo real el ángulo de elevación de mi brazo, **para** conocer mi rango de movimiento. | 5 | Sprint 4 |
| **US-05** | Conteo Automático de Repeticiones | **Como** usuario, **quiero** que el sistema cuente automáticamente cada vez que complete una elevación lateral válida, **para** saber cuántas llevo sin distraerme. | 5 | Sprint 5 |
| **US-06** | Retroalimentación de Corrección | **Como** usuario, **quiero** recibir un mensaje claro (ej., "Levante más el brazo") cuando mi movimiento sea incorrecto, **para** corregirlo en el momento. | 8 | Sprint 6 |
| **T-07** | Diseño del Protocolo de Validación | **Como** investigador, **quiero** definir el protocolo experimental con *baseline* (goniómetro), **para** poder validar el sistema. | 3 | Sprint 7 |
| **T-08** | Pruebas de Validación y Recolección de Datos | **Como** investigador, **quiero** ejecutar el protocolo con sujetos de prueba, **para** obtener métricas de rendimiento. | 8 | Sprint 8 |
| **T-09** | Análisis de Datos y Generación de Gráficos | **Como** investigador, **quiero** analizar los datos y crear gráficas comparativas, **para** evaluar si el sistema cumple los criterios de éxito. | 5 | Sprint 9 |
| **US-10** | Exportación de Reportes | **Como** usuario/terapeuta, **quiero** exportar un archivo (CSV/PDF) con mi sesión (repeticiones, ángulos máximos), **para** llevar un registro. | 5 | Sprint 10 (si hay tiempo) |

Los criterios de aceptación detallados por historia se documentan en el Anexo B. **Objetivos e incrementos por sprint:** Cada sprint produce un incremento funcional verificable: Sprints 1–2 (entorno y captura operativa); 3–4 (detección de pose y ángulo visible); 5–6 (conteo y retroalimentación completos); 7 (protocolo de validación); 8–10 (estabilización y exportación); 11–14 (ejecución del protocolo y análisis); 15–16 (documentación final).

### **4.3. Definiciones de Ready/Done**
Estas definiciones operativas garantizan la calidad y claridad antes de iniciar y al finalizar cada tarea.

*   **Definición de Listo (Definition of Ready - DoR):** Una historia de usuario está **"Lista"** para ser incorporada a un Sprint cuando:
    1.  Está claramente descrita y sus criterios de aceptación son conocidos por el equipo.
    2.  Tiene dependencias identificadas y resueltas.
    3.  Ha sido estimada por el equipo.
    4.  Es lo suficientemente pequeña para ser completada en un Sprint.

*   **Definición de Hecho (Definition of Done - DoD):** Una historia de usuario está **"Hecha"** cuando:
    1.  El código está escrito, documentado y cumple con los estándares acordados.
    2.  La funcionalidad ha sido integrada con el resto del sistema.
    3.  Se han ejecutado pruebas unitarias y de integración, obteniendo resultados satisfactorios.
    4.  El código ha sido revisado por al menos otro miembro del equipo (peer review).
    5.  Se ha actualizado la documentación relevante (comentarios en código, README del repositorio).

### **4.4. Principios Lean, Ciclo Operativo y Métricas**
La filosofía **Lean** se integra para centrar el esfuerzo en generar valor y eliminar desperdicios. Se aplican tres principios clave:
1.  **Construir-Medir-Aprender:** Cada Sprint debe producir un incremento funcional (**Construir**), que será medido objetivamente (precisión, latencia) o mediante *feedback* (**Medir**), para extraer aprendizajes que guíen la siguiente iteración (**Aprender**).
2.  **Validated Learning (Aprendizaje Validado):** Las decisiones de desarrollo (ej., elegir MediaPipe sobre OpenPose) deben estar validadas por experimentos rápidos o *benchmarks* técnicos, no por suposiciones.
3.  **Innovación Continua (Kaizen):** Se fomenta la mejora continua tanto del producto (en cada Sprint Review) como del proceso (en cada Sprint Retrospective).

**Ciclo Lean aplicado por sprint:** En cada iteración se ejecuta el ciclo operativo siguiente: (1) **Medir:** velocidad (puntos completados), bug rate post-DoD y valor cualitativo del Product Owner; (2) **Instrumento:** tablero de tareas (p. ej. Trello o Jira), repositorio Git con historial de commits, bitácora de pruebas; (3) **Umbrales de ajuste:** si la velocidad cae >20% respecto al promedio de dos sprints previos, se revisa el alcance; si el bug rate supera 2 críticos por historia cerrada, se refuerza el DoD; si el Product Owner califica el incremento por debajo de "valor moderado", se prioriza en el siguiente sprint; (4) **Decisión:** continuar con el plan o ajustar backlog/alcance según los umbrales. De este modo, cada sprint concluye con una decisión explícita de continuar o pivotar.

Las **Métricas Lean** que se rastrearán son:
*   **Velocidad del Equipo:** Promedio de puntos de historia completados por Sprint. Ayuda a prever la capacidad de trabajo futura.
*   **Tasa de Error en Detección (Bug Rate):** Número de errores críticos encontrados después de que una funcionalidad se marcó como "Hecha". Indica la calidad del DoD.
*   **Valor de Negocio Entregado:** Evaluación cualitativa del Product Owner sobre cuánto valor aportó el incremento de cada Sprint hacia el objetivo general del proyecto.
*   **Cumplimiento de Criterios de Éxito:** Progreso hacia los umbrales numéricos definidos (MAE < 5°, precisión > 95%), que es la métrica de valor final.

### **4.5. Herramientas de Seguimiento y Evidencia**
Para sostener la trazabilidad y demostrar la ejecución del proyecto, el equipo utilizará las siguientes herramientas: (1) **Tablero de tareas** (Trello, Jira o equivalente): visualización del backlog, sprint backlog y estado de cada ítem; (2) **Repositorio Git** (GitHub): código fuente, historial de commits, ramas de características y *pull requests*; (3) **Bitácora o registro de pruebas:** documentación de las pruebas unitarias, de integración y de usabilidad realizadas, con resultados; (4) **Carpeta de evidencias:** capturas de pantalla del prototipo, logs de sesión anonimizados y gráficos de análisis de validación. Estas herramientas permiten auditar el cumplimiento del DoD y la trazabilidad objetivo–evidencia.

\newpage

## **5. IMPLEMENTACIÓN DE LA PROPUESTA**

Se describe la ejecución práctica del proyecto: arquitectura técnica, componentes, entorno de desarrollo, despliegue y mantenimiento del prototipo.

### **5.1. Planificación y Estimación (Tiempo/Costo)**
La implementación se realizará en el plazo estricto de 16 semanas, asignando las primeras 12 al desarrollo del prototipo y las 4 finales a la validación experimental, documentación y preparación de la entrega final. La estimación de costos se basa en el principio de **máximo aprovechamiento de recursos de código abierto y hardware existente**.

*   **Cronograma Detallado (Sprints de 1 semana):**
    *   **Sprints 1-2:** Configuración del entorno (Python 3.9, Git), investigación profunda de MediaPipe/OpenCV, y definición de la arquitectura de software.
    *   **Sprints 3-4:** Desarrollo del módulo de captura de video y la integración básica del modelo MediaPipe Pose (`pose_landmarker_lite` por defecto). Primer prototipo que muestra puntos clave en video.
    *   **Sprints 5-6:** Implementación del cálculo geométrico del ángulo de hombro y la máquina de estados para el conteo de repeticiones.
    *   **Sprints 7-8:** Desarrollo de la interfaz gráfica (GUI) integrada y el sistema de retroalimentación por texto/color.
    *   **Sprints 9-10:** Estabilización del código, pruebas internas de usabilidad y depuración. Creación del protocolo de validación y materiales (hojas de registro, consentimiento informado).
    *   **Sprints 11-12:** Ejecución del protocolo experimental: captura de videos de prueba y recolección de datos de *baseline* (goniómetro, conteo manual).
    *   **Sprints 13-14:** Análisis de datos, cálculo de métricas (MAE, precisión) y generación de gráficos comparativos.
    *   **Sprints 15-16:** Redacción final del documento académico, preparación del video de presentación y consolidación del repositorio Git.

*   **Estimación de Costos:**
    *   **Costos Directos Cero (€0):** Todo el software es de código abierto (Python, OpenCV, MediaPipe, librerías de análisis). No se requiere compra de hardware especializado, asumiendo que el equipo cuenta con una computadora personal y una cámara web (equipos ya disponibles).
    *   **Costos Indirectos:** Se invertirá aproximadamente **20 horas/semana por integrante** en el proyecto, lo que representa la principal inversión de recursos (tiempo y esfuerzo intelectual). Esta inversión se considera parte del trabajo académico de la maestría.

### **5.2. Implementación (Arquitectura, Datos, Componentes, Repositorio)**
El sistema usará una **arquitectura modular monolítica** en Python para facilitar el mantenimiento y la lectura del código.

*   **Arquitectura del Sistema:**
    ```
    [Cámara Web] → Módulo de Captura (OpenCV) → Módulo de Detección de Pose (MediaPipe)
                          ↓
        [Interfaz Gráfica (GUI)] ← Módulo de Lógica de Aplicación ← Módulo de Cálculo (Geometría)
        (Visualización + Feedback)  (Control de Estado, Conteo)      (Cálculo de Ángulos)
                          ↓
                   [Salida: Video Anotado + Métricas]
    ```

*   **Componentes Tecnológicos Clave:**
    *   **Lenguaje y Entorno:** Python 3.9+, utilizando entornos virtuales (`venv`) para gestionar dependencias. El IDE principal será Visual Studio Code.
    *   **Librerías Principales:**
        *   **OpenCV (`cv2`)**: Para captura de video, procesamiento de imágenes básico y visualización de la GUI.
        *   **MediaPipe (`mediapipe`)**: Para la estimación de pose 2D con el modelo preentrenado (por defecto `pose_landmarker_lite.task`; opcional `pose_landmarker_full.task`).
        *   **NumPy:** Para todos los cálculos matemáticos y vectoriales eficientes.
        *   **Pandas & Matplotlib/Seaborn:** Para el análisis de datos de las sesiones de validación y la generación de gráficos.
    *   **Gestión de Datos:** Las sesiones (ángulos por *frame*, repeticiones, timestamps) se almacenan en **CSV** locales. No se guardan videos crudos; solo secuencias anonimizadas para validación, con consentimiento explícito.
    *   **Repositorio de Código:** Código en **Git** (repositorio privado en GitHub): `/src`, `/docs`, `/data` (CSV de ejemplo, sin datos personales), `/tests` y `README.md`.

### **5.3. Despliegue (Entorno, Seguridad, Contingencia)**
*   **Entorno de Despliegue:** El MVP está diseñado para ejecutarse localmente en sistemas operativos **Windows 10/11** y **macOS** (y potencialmente Linux). Se entregará como un script Python ejecutable, con instrucciones claras para instalar dependencias vía `requirements.txt`.
*   **Seguridad y Privacidad:** La privacidad constituye un pilar del diseño. Al ejecutarse **íntegramente en la computadora local**, se garantiza que:
    1.  El video del paciente nunca abandona su dispositivo.
    2.  No hay dependencia de conexión a Internet durante el uso.
    3.  Los datos de rendimiento (CSV) se guardan localmente, bajo el control total del usuario.
    4.  Se implementará un mensaje claro de consentimiento informado al iniciar la aplicación por primera vez.
*   **Plan de Contingencia:** Los principales riesgos son técnicos (inestabilidad de MediaPipe en ciertas poses o iluminación). La contingencia incluye:
    1.  **Backup de código:** Commits diarios y ramas de características en Git.
    2.  **Fallback visual:** Si la detección de pose falla, la GUI mostrará un mensaje claro indicando cómo re-posicionarse, en lugar de fallar silenciosamente.
    3.  **Documentación de errores:** Un archivo `KNOWN_ISSUES.md` documentará limitaciones conocidas.

### **5.4. Mantenimiento (Cambios, Versionado)**
*   **Estrategia de Versionado:** Se seguirá **Versionado Semántico (SemVer)** para posibles releases futuras: `MAJOR.MINOR.PATCH` (ej., v1.0.0 para el MVP final). Los cambios se gestionarán a través de ramas en Git y *Pull Requests*.
*   **Mantenimiento Post-Proyecto:** Aunque el desarrollo formal concluye con el seminario, se deja establecida una base de código limpia y documentada que permita:
    1.  La adición de nuevos ejercicios (p. ej., flexión de codo) mediante módulos.
    2.  La mejora de la GUI con librerías más avanzadas (p. ej., Tkinter, PyQt).
    3.  La integración de un perfil de usuario simple para guardar historiales.
*   **Sostenibilidad:** La dependencia de tecnologías de código abierto maduras (Python, OpenCV) asegura que el prototipo no quedará obsoleto rápidamente y podrá ser ejecutado en equipos futuros.

\newpage

## **6. VALIDACIÓN Y DISEÑO EXPERIMENTAL**

El diseño experimental evalúa el rendimiento del sistema mediante comparación con un *baseline* de referencia (goniómetro, conteo humano), con métricas reproducibles.

### **6.1. Hipótesis**
Las hipótesis, alineadas con los objetivos y criterios de éxito, son:

1.  **Hipótesis Principal (H1):** El sistema de visión por computadora logrará medir el ángulo de abducción del hombro con una precisión comparable a la medición manual con goniómetro, manifestándose en un **Error Absoluto Medio (MAE) igual o inferior a 5 grados**.
2.  **Hipótesis Secundaria (H2):** El algoritmo de conteo automático identificará correctamente las repeticiones válidas de elevación lateral del brazo, alcanzando una **precisión igual o superior al 95%** en comparación con el conteo realizado por un evaluador humano.
3.  **Hipótesis Operativa (H3):** La latencia total del sistema, desde la captura del *frame* de video hasta la visualización de la retroalimentación en pantalla, será **inferior a 150 milisegundos**, permitiendo una experiencia de uso en tiempo real.

### **6.2. Métricas de Evaluación**
Se usan métricas estándar en visión por computadora y evaluación de sistemas (Tabla 5):

*   **Precisión en la Medición Angular:** Se utilizará el **Error Absoluto Medio (MAE)**. Para cada repetición válida, se calculará la diferencia absoluta entre el ángulo máximo reportado por el sistema y el ángulo máximo medido con el goniómetro. El MAE es el promedio de estos errores a través de todas las repeticiones de todos los sujetos.
    *   **Fórmula:** `MAE = (1/n) * Σ |ángulo_sistema_i - ángulo_goniómetro_i|`
    *   **Criterio de Éxito:** MAE ≤ 5°.

*   **Precisión en el Conteo de Repeticiones:** Se calculará como el porcentaje de repeticiones correctamente identificadas por el sistema frente al total de repeticiones reales validadas por el evaluador humano.
    *   **Fórmula:** `Precisión = (Repeticiones Correctamente Contadas / Total de Repeticiones Reales) * 100%`
    *   **Criterio de Éxito:** Precisión ≥ 95%.

*   **Latencia del Sistema:** Se medirá como el tiempo transcurrido entre un evento de movimiento claramente definido (ej., el instante en que la mano pasa por un punto de referencia marcado) y la actualización correspondiente en la interfaz de usuario (ej., cambio en el contador o aparición de un mensaje de corrección). Se medirá utilizando marcas de tiempo de alta resolución.
    *   **Criterio de Éxito:** Latencia < 150 ms.

*Tabla 5. Resumen de métricas, baselines y criterios de éxito.*
| **Métrica** | **Definición** | **Baseline / Método de Referencia** | **Criterio de Éxito para la Validación** |
| :--- | :--- | :--- | :--- |
| **Error Angular (MAE)** | Diferencia promedio absoluta entre el ángulo medido por el sistema y el ángulo de referencia. | Medición con goniómetro manual estándar por un evaluador. | **MAE ≤ 5.0°** |
| **Precisión en Conteo** | Porcentaje de repeticiones correctamente contadas por el sistema. | Conteo visual y manual realizado por un evaluador humano desde el video grabado. | **Precisión ≥ 95%** |
| **Latencia** | Retraso entre un evento de movimiento y su retroalimentación en pantalla. | Mediciones manuales con cronómetro de alta precisión sobre video grabado a alta velocidad (60 FPS). | **Latencia < 150 ms** |
| **Robustez (Cualitativa)** | Capacidad del sistema de funcionar bajo variaciones de iluminación y vestimenta. | Observación y registro de fallos durante las pruebas en condiciones diversas. | Funcionamiento estable en al menos 3 condiciones de iluminación diferentes. |

### **6.3. Protocolo Experimental**
El protocolo persigue reproducibilidad y validez interna. Fases:

**1. Preparación y Reclutamiento:**
*   Se reclutarán **5 sujetos sanos adultos** (3 hombres, 2 mujeres) mediante muestreo por conveniencia, todos diestros y sin historial de patología en el hombro derecho. La elección de sujetos sanos para esta fase de validación técnica es estándar, ya que permite controlar variables y establecer la precisión base del sistema antes de pruebas con pacientes clínicos.
*   Cada participante firmará un **formulario de consentimiento informado** (ver Anexo A) que detalla el propósito académico, el anonimato de sus datos y el procesamiento local de las imágenes.

**2. Configuración y Calibración:**
*   El sujeto se colocará de pie a 2 metros de una cámara web Logitech C920 (1080p, 30 FPS), con iluminación ambiente uniforme.
*   Se marcarán los puntos anatómicos de referencia (acromion para el hombro, epicóndilo lateral para el codo) en la piel del sujeto para facilitar la medición con goniómetro.
*   Un evaluador entrenado se colocará en posición para realizar mediciones con goniómetro sin obstruir la vista de la cámara.

**3. Ejecución y Captura de Datos:**
*   Cada sujeto realizará **3 series de 10 repeticiones** de abducción de hombro en el plano frontal (elevación lateral del brazo), a un ritmo constante guiado por un metrónomo (1 repetición cada 3 segundos).
*   **Datos del Sistema:** El prototipo grabará un archivo de log con: timestamp de cada *frame*, coordenadas de los *landmarks*, ángulo calculado, estado de la repetición y cualquier mensaje de retroalimentación generado.
*   **Datos de Baseline (Verdad de Campo):**
    *   **Ángulo:** El evaluador medirá y registrará manualmente el ángulo máximo alcanzado en **cada repetición** utilizando un goniómetro de brazos largos.
    *   **Conteo:** Un segundo evaluador, o el mismo revisando el video grabado, contará las repeticiones válidas (ciclo completo que supere los 60°).

**4. Análisis de Datos:**
*   Los datos del sistema (CSV) y los datos manuales (hoja de cálculo) se sincronizarán usando los timestamps.
*   Un script de análisis en Python (usando Pandas y SciPy) calculará automáticamente las métricas definidas: MAE por sujeto y global, precisión de conteo y latencia.
*   Se generarán gráficos de dispersión (ángulo sistema vs. ángulo goniómetro), gráficos de series temporales de ángulo y tablas de resumen.

### **6.4. Resultados Esperados y Discusión**
*   **Resultados esperados:** Se espera MAE entre 3° y 5°, precisión de conteo del 96-100% y latencia < 100 ms en equipo de gama media.
*   **Análisis de errores:** Se revisarán repeticiones y sujetos con mayor error. Fuentes probables: (1) error de paralaje en la medición con goniómetro; (2) oclusión parcial del hombro por la mano frente a la cámara; (3) variabilidad entre repeticiones.
*   **Limitaciones:** Población sana (sin compensaciones típicas post-ACV), entorno controlado (no domicilio real) y muestra pequeña; válido para prueba de concepto técnica, no para generalización clínica.
*   **Validez y confiabilidad:** El protocolo controla distancia, iluminación y ritmo (validez interna). Las mediciones objetivas y automatizadas son replicables.

\newpage

## **7. CONCLUSIONES Y TRABAJO FUTURO**

### **7.1. Conclusiones**

El trabajo ha diseñado y planificado un **sistema de asistencia para rehabilitación motriz domiciliaria post-ACV basado en visión por computadora**, que responde al reto de diseño (*¿cómo proporcionar una herramienta accesible con supervisión objetiva?*) con un enfoque centrado en accesibilidad, viabilidad técnica y privacidad.

La aplicación de **Design Thinking** permitió anclar la solución en las necesidades de pacientes y terapeutas y en la brecha de supervisión objetiva en el hogar. El estado del arte mostró un hueco para una solución práctica y escalable que combine software de IA de código abierto con hardware de consumo, sin depender de dispositivos costosos.

**Scrum** y **Lean Startup** estructuran un plan de ejecución realista: desarrollo del prototipo (Python, OpenCV, MediaPipe) en 16 semanas, con entregas incrementales y un **MVP** bien acotado.

El diseño experimental aporta hipótesis comprobables, métricas objetivas (MAE ≤ 5°, precisión ≥ 95%) y *baseline* con goniómetro, de modo que el proyecto va más allá de la mera descripción y puede generar evidencia reproducible. En conjunto, la propuesta resulta viable técnicamente y pertinente para ampliar el acceso a rehabilitación de calidad.

### **7.2. Limitaciones y Trabajo Futuro**

La propuesta tiene limitaciones claras que conviene tener presentes:

*   **Limitaciones del Proyecto Actual:**
    1.  **Validación con Población Simulada:** El protocolo de validación se ejecutará con sujetos sanos. Si bien esto es válido para la prueba de concepto técnica, no captura las complejidades del movimiento patológico, las compensaciones o la fatiga en pacientes reales post-ACV.
    2.  **Alcance Clínico Reducido:** El MVP se centra en un solo ejercicio (abducción de hombro). Una herramienta clínicamente útil requeriría una biblioteca de ejercicios para diferentes articulaciones y déficits.
    3.  **Entorno Controlado:** Las pruebas se realizan en condiciones de iluminación y fondo optimizadas. La robustez del sistema en entornos domésticos diversos (distintas habitaciones, iluminación cambiante) no se ha evaluado.

*   **Trabajo futuro:** Para acercar el prototipo al impacto clínico real, se sugieren estas líneas:
    1.  **Estudio Piloto con Pacientes:** El siguiente paso esencial es un **estudio piloto de viabilidad** con un pequeño grupo (n=5-10) de pacientes reales en fase subaguda o crónica post-ACV. Esto permitiría evaluar la usabilidad, la aceptación y ajustar los umbrales de movimiento a las capacidades reales de los usuarios.
    2.  **Ampliación de la Biblioteca de Ejercicios:** Desarrollo de módulos para ejercicios clave de la extremidad superior (flexión/extensión de codo, protracción/retracción escapular) e inferior (flexión de rodilla, dorsiflexión de tobillo), basados en protocolos de rehabilitación estandarizados.
    3.  **Personalización y Adaptabilidad:** Implementación de algoritmos que permitan al sistema **ajustarse automáticamente** al rango de movimiento inicial del paciente y aumentar progresivamente la dificultad de los ejercicios (entrenamiento adaptativo), tal como lo haría un terapeuta.
    4.  **Integración con Historial Clínico Electrónico (HCE):** Diseño de un módulo de exportación segura de datos (usando estándares como FHIR) que permita al sistema enviar reportes estructurados de progreso directamente a la historia clínica del paciente, facilitando la supervisión remota del terapeuta.
    5.  **Investigación de Robustez Técnica:** Experimentación con técnicas de **aprendizaje por transferencia** (*transfer learning*) para afinar el modelo de estimación de pose (MediaPipe) con datos de pacientes con movimientos atípicos, mejorando su precisión en condiciones reales.

El proyecto funciona como punto de partida para abordar un problema de salud complejo con un enfoque pragmático y centrado en el usuario. Las líneas de trabajo futuro apuntan a llevar esta innovación hacia una solución tecnológica que contribuya a la recuperación y la calidad de vida de personas post-ACV.

\newpage

## **8. REFERENCIAS**

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.).

Basteris, A., Nijenhuis, S. M., Stienen, A. H., Buurke, J. H., Prange, G. B., & Amirabdollahian, F. (2014). Training modalities in robot-mediated upper limb rehabilitation in stroke: A framework for classification based on a systematic review. *Journal of NeuroEngineering and Rehabilitation, 11*(1), 111. https://doi.org/10.1186/1743-0003-11-111

Cao, Z., Hidalgo, G., Simon, T., Wei, S.-E., & Sheikh, Y. (2021). OpenPose: Realtime multi-person 2D pose estimation using part affinity fields. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 43*(1), 172–186. https://doi.org/10.1109/TPAMI.2019.2929257

Debnath, B., O'Brien, M., Yamaguchi, M., & Behera, A. (2021). A review of computer vision-based approaches for physical rehabilitation and assessment. *Multimedia Systems*, *28*, 209–239. https://doi.org/10.1007/s00530-021-00815-4

Esteva, A., Robicquet, A., Ramsundar, B., Kuleshov, V., DePristo, M., Chou, K., Cui, C., Corrado, G., Thrun, S., & Dean, J. (2019). A guide to deep learning in healthcare. *Nature Medicine, 25*(1), 24–29. https://doi.org/10.1038/s41591-018-0316-z

Instituto Nacional de Estadística y Geografía. (2021). *Estadísticas de defunciones registradas 2020*. https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2021/EstSociodemo/DefuncionesRegistradas2020_Pnles.pdf

Langhorne, P., Bernhardt, J., & Kwakkel, G. (2011). Stroke rehabilitation. *The Lancet*, *377*(9778), 1693–1702. https://doi.org/10.1016/S0140-6736(11)60325-5

Laver, K. E., Adey-Wakeling, Z., Crotty, M., Lannin, N. A., George, S., & Sherrington, C. (2020). Telerehabilitation services for stroke. *Cochrane Database of Systematic Reviews, 1*(1), CD010255. https://doi.org/10.1002/14651858.CD010255.pub3

Organización Mundial de la Salud (OMS). (2017). *Rehabilitation in health systems*. https://apps.who.int/iris/handle/10665/254506

Saposnik, G., Cohen, L. G., Mamdani, M., Pooyania, S., Ploughman, M., Cheung, D., Shaw, J., Hall, J., Nord, P., Dukelow, S., Nilanont, Y., De Los Rios, F., Olmos, L., Levin, M., Teasell, R., Cohen, A., Thorpe, K., Laupacis, A., & Bayley, M. (2016). Efficacy and safety of non-immersive virtual reality exercising in stroke rehabilitation (EVREST): A randomised, multicentre, single-blind, controlled trial. *The Lancet Neurology, 15*(10), 1019–1027. https://doi.org/10.1016/S1474-4422(16)30121-1

\newpage

## **9. ANEXOS**

Los anexos se detallan en documentos independientes en la carpeta `anexos/`. A continuación se describe el contenido de cada uno.

**Anexo A: Formulario de Consentimiento Informado para Participantes en la Fase de Validación**
Documento modelo que será presentado a los sujetos sanos reclutados para la prueba experimental. Incluirá: objetivo del estudio, descripción de la participación (grabación en video para análisis técnico), garantías de anonimato y procesamiento local de datos, riesgos y beneficios, y declaración de consentimiento voluntario.

**Anexo B: Backlog Completo del Producto y Planificación de Sprints**
Tabla detallada que expande la presentada en el Capítulo 4. Incluirá todas las historias de usuario (US) y tareas técnicas (T) desglosadas, con su identificación única (ID), descripción completa, criterios de aceptación, puntos de historia asignados y el Sprint en el que fueron planificadas y completadas.

**Anexo C: Diagramas de Arquitectura y Bocetos de Interfaz (Wireframes)**
Ilustraciones técnicas que complementan la descripción textual del Capítulo 5.
1.  Diagrama de flujo detallado del *pipeline* de procesamiento del sistema.
2.  Bocetos de baja fidelidad (*wireframes*) de la interfaz gráfica principal, mostrando la disposición de los elementos: ventana de video, superposición del esqueleto, panel de métricas en tiempo real (ángulo, contador) y área de mensajes de retroalimentación.

**Anexo D: Protocolo Experimental Operativo**
Documento paso a paso utilizado durante la fase de validación (Capítulo 6). Contendrá:
1.  Lista de verificación (*checklist*) de preparación (equipo, software, sala).
2.  Guión estandarizado de instrucciones para los participantes.
3.  Plantilla de hoja de registro en papel para las mediciones manuales con goniómetro y conteo humano.
4.  Procedimiento para la sincronización de datos y el backup de archivos.

**Anexo E: Ejemplos de Salida del Sistema y Datos Crudos (Anonimizados)**
Muestra representativa y anonimizada de los datos generados por el prototipo, destinada a ilustrar su funcionamiento.
1.  Captura de pantalla del sistema en funcionamiento durante una repetición.
2.  Extracto de un archivo de log CSV generado por el sistema, mostrando las columnas de datos (timestamp, coordenadas, ángulo calculado, estado de la repetición).
3.  Ejemplo de un gráfico de evolución del ángulo en el tiempo generado por el módulo de análisis (usando Matplotlib/Seaborn).

**Anexo F: Repositorio de Código y Documentación Técnica**
Este anexo consistirá en una nota que indica la URL del repositorio Git privado donde residirá el código fuente completo del proyecto. Se hará referencia a que el repositorio contiene:
1.  El código fuente comentado de todos los módulos.
2.  El archivo `README.md` con instrucciones de instalación y uso.
3.  El archivo `requirements.txt` con las dependencias de Python.
4.  Los scripts de análisis de datos utilizados en la validación.
*(Nota: La URL real se insertará al momento de la entrega final del proyecto).*
