# Evidencias Jira — Gestión del proyecto

Capturas de pantalla de la instancia Jira local usada para el seguimiento del backlog (épicas, historias de usuario y tareas). Se toman con Jira en ejecución en `http://localhost:8080`.

## Cómo generar Jira local, datos y capturas

1. **Levantar Jira:** `docker compose -f docker-compose.jira.yml up -d` (o `docker start jira-rehab`). Jira tarda 2–5 minutos en estar listo.
2. **Primera vez (obligatorio):** Abre http://localhost:8080 y **completa el asistente**: idioma, licencia de evaluación, usuario y contraseña admin. Luego crea un **proyecto Scrum** con clave **REHAB** (Epic, Story y Task habilitados). Sin esto, la API devuelve 503 y no se pueden insertar datos ni sacar capturas.
3. **Verificación:** Ejecuta `./scripts/jira_verificar.sh` para comprobar Docker, API, datos y capturas. Si pasas la contraseña (`./scripts/jira_verificar.sh tu_password`) y Jira está listo, el script te indicará el comando para inyectar y capturar.
4. **Inyectar datos:** Con el proyecto REHAB ya creado: `JIRA_PASS=<tu_admin_pass> npm run jira:inject`. Alternativa: importa en Jira (Backlog → Importar desde CSV) primero `jira_import_epics.csv`, luego `jira_import_issues.csv`.
5. **Asignar al sprint (board con datos):** Para que el board muestre tareas y épicas en un sprint activo, ejecuta `npm run jira:sprint`. Crea o reutiliza el sprint "Sprint 1 - Prototipo core", asigna las issues (US-01 a US-10, T-07 a T-09) y marca como Done las ya implementadas en `rehab_cv` (prototipo core, exportación, protocolo, análisis). T-08 queda en To Do/En progreso.
6. **Sacar capturas (automático):**
   ```bash
   JIRA_URL=http://localhost:8080 JIRA_USER=admin JIRA_PASS=<tu_admin_pass> npm run jira:capture
   ```
   **Todo en uno** (esperar a Jira + inyectar + capturar): después de crear el proyecto REHAB en el navegador, ejecuta:
   ```bash
   JIRA_PASS=admin ./scripts/jira_wait_inject_capture.sh
   ```
   Las imágenes se guardan aquí con los nombres indicados abajo. También puedes hacer las capturas a mano desde el navegador.

7. **Capturas aseguradas (con o sin Jira listo):** `npm run jira:ensure` intenta inyectar datos y capturar; si Jira no está listo (503), genera imágenes placeholder con instrucciones. Así el documento siempre puede incluir `jira_board_backlog.png` y `jira_board_sprint.png`.

## Imágenes a incluir

| Archivo | Descripción |
|---------|-------------|
| `jira_board_backlog.png` | Vista del backlog: épicas E1–E3 y debajo las stories/tasks con prioridad y sprint. |
| `jira_board_sprint.png` | Board del sprint activo (o Sprint 1): columnas Por hacer / En progreso / Hecho con tarjetas. |
| `jira_epic_detail.png` | Detalle de una épica (ej. E1): título, descripción, lista de issues enlazadas (US-01 a US-06). |
| `jira_story_detail.png` | Detalle de una story (ej. US-04 o US-06): título, criterios, story points, epic, sprint. |
| `jira_roadmap_or_timeline.png` | (Opcional) Roadmap / Timeline por épicas y sprints si está disponible. |

Guardar en PNG o JPG con resolución suficiente (ej. 1920×1080 o 1280×720) para que se lean bien en el PDF.
