#!/usr/bin/env bash
# Poblar Jira local con épicas, historias de usuario y tareas del proyecto.
# Requisitos: Jira en ejecución (ej. docker compose -f docker-compose.jira.yml up -d)
#             y proyecto Scrum creado en la UI (clave ej. REHAB) con Epic, Story, Task.
# Uso:
#   1) Generar CSV para importar en Jira: ./scripts/jira_seed.sh --csv
#   2) Usar jira-cli (si está configurado): export JIRA_PROJECT=REHAB; ./scripts/jira_seed.sh --cli
# CSV: Jira > Proyecto > Backlog > ... (menú) > Importar desde CSV.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="${REPO_ROOT}/docs/evidencias_jira"
CSV_EPICS="${OUTPUT_DIR}/jira_import_epics.csv"
CSV_ISSUES="${OUTPUT_DIR}/jira_import_issues.csv"

mkdir -p "$OUTPUT_DIR"

# ---------------------------------------------------------------------------
# Generar CSV para importación en Jira (Backlog > Importar desde CSV)
# Importar primero jira_import_epics.csv, luego jira_import_issues.csv
# y mapear columnas a Summary, Description, Issue Type, Epic Name, etc.
# ---------------------------------------------------------------------------
generate_csv() {
  # Epics (importar primero)
  cat > "$CSV_EPICS" << 'EPICS'
Summary,Description,Issue Type
E1: Prototipo core,"Entorno, captura, pose, ángulo, conteo, feedback. Contiene US-01 a US-06.",Epic
E2: Validación experimental,"Protocolo, pruebas y análisis. Contiene T-07, T-08, T-09.",Epic
E3: Entrega y documentación,"Entrega y documentación. Contiene US-10.",Epic
EPICS

  # Stories y Tasks (Issue Type, Summary, Description, Epic Name, Story Points, Sprint/Labels)
  # Epic Name debe coincidir con el Summary del Epic en Jira tras importar epics.
  cat > "$CSV_ISSUES" << 'ISSUES'
Summary,Description,Issue Type,Epic Name,Story Points
US-01 Configuración del entorno,"(1) venv creado; (2) requirements.txt con opencv-python, mediapipe, numpy; (3) script de prueba que importa librerías; (4) proyecto en Git con /src, /docs, /data.",Story,E1: Prototipo core,1
US-02 Captura de video en tiempo real,"(1) Captura con OpenCV desde cámara por defecto; (2) ventana con video en vivo; (3) cierre correcto; (4) resolución 720p o superior.",Story,E1: Prototipo core,2
US-03 Visualización del esqueleto,"(1) MediaPipe Pose integrado; (2) dibujo de landmarks y conexiones; (3) hombro, codo y cadera visibles; (4) integrado con ventana de video US-02.",Story,E1: Prototipo core,3
US-04 Cálculo y visualización de ángulo,"(1) Ángulo de abducción (cadera-hombro-codo); (2) valor en grados visible; (3) actualización frame a frame; (4) código documentado.",Story,E1: Prototipo core,5
US-05 Conteo automático de repeticiones,"(1) Máquina de estados subida/bajada; (2) umbrales configurables (ej. 60°); (3) contador visible; (4) sin falsos positivos evidentes.",Story,E1: Prototipo core,5
US-06 Retroalimentación de corrección,"(1) Mensajes según reglas; (2) criterios por umbrales; (3) mensajes en zona dedicada; (4) integración con conteo.",Story,E1: Prototipo core,8
T-07 Diseño del protocolo de validación,"(1) Documento con hipótesis, métricas y criterios; (2) fases: reclutamiento, configuración, ejecución, análisis; (3) materiales y revisión.",Task,E2: Validación experimental,3
T-08 Pruebas de validación y datos,"(1) Al menos 5 sujetos; (2) consentimiento firmado; (3) 3×10 repeticiones con goniómetro y grabación; (4) logs CSV y backup.",Task,E2: Validación experimental,8
T-09 Análisis y gráficos,"(1) Script que calcula MAE, precisión y latencia; (2) gráficos y tablas; (3) informe con resultados y limitaciones.",Task,E2: Validación experimental,5
US-10 Exportación de reportes,"(1) Exportación a CSV; (2) opción PDF si hay tiempo; (3) archivos en carpeta local; (4) documentado en README.",Story,E3: Entrega y documentación,5
ISSUES

  echo "CSV generados:"
  echo "  - $CSV_EPICS (importar primero en Jira: Backlog > Importar desde CSV)"
  echo "  - $CSV_ISSUES (importar después; mapear 'Epic Name' al campo Epic del proyecto)"
}

# ---------------------------------------------------------------------------
# Crear issues vía jira-cli (ankitpokhrel/jira-cli o go-jira)
# Configurar: jira init (host http://localhost:8080, usuario/contraseña)
# Exportar: JIRA_PROJECT=REHAB
# ---------------------------------------------------------------------------
run_cli() {
  if ! command -v jira &>/dev/null; then
    echo "No se encontró el comando 'jira'. Instalar con: npm i -g jira-cli"
    echo "O usar solo importación CSV: $0 --csv"
    exit 1
  fi
  PROJECT="${JIRA_PROJECT:-REHAB}"
  echo "Usando proyecto Jira: $PROJECT"
  # Crear épicas (en jira-cli suele ser: jira issue create -t Epic -s "..." -p "$PROJECT")
  for title in "E1: Prototipo core" "E2: Validación experimental" "E3: Entrega y documentación"; do
    jira issue create -t Epic -s "$title" -p "$PROJECT" || true
  done
  echo "Épicas creadas (o ya existían). Crear Stories y Tasks desde la UI o importar CSV."
  echo "Para enlazar a épica: jira epic add <EPIC-KEY> <ISSUE-KEY>"
}

# ---------------------------------------------------------------------------
case "${1:-}" in
  --csv)  generate_csv ;;
  --cli)  run_cli ;;
  *)      generate_csv
          echo ""
          echo "Opciones: --csv (solo generar CSV) | --cli (crear vía jira-cli)"
          ;;
esac
