#!/usr/bin/env bash
# Espera a que Jira responda, inyecta épicas/issues y saca capturas.
# Uso: JIRA_PASS=admin ./scripts/jira_wait_inject_capture.sh
# Requisito: haber completado el asistente de Jira y creado el proyecto REHAB.

set -e
JIRA_URL="${JIRA_URL:-http://localhost:8080}"
JIRA_USER="${JIRA_USER:-admin}"
JIRA_PASS="${JIRA_PASS:?Indica JIRA_PASS=tu_contraseña}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "Esperando a que Jira responda en $JIRA_URL..."
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$JIRA_URL/rest/api/2/serverInfo" 2>/dev/null || true)
  if [ "$code" = "200" ] || [ "$code" = "401" ]; then
    echo "Jira listo (HTTP $code)."
    break
  fi
  [ $i -eq 30 ] && { echo "Timeout: Jira no respondió. ¿Completaste el asistente en el navegador?"; exit 1; }
  echo "  Intento $i: $code (esperando 10s)..."
  sleep 10
done

echo "Inyectando épicas e issues..."
export JIRA_URL JIRA_USER JIRA_PASS
node scripts/jira_inject.mjs

echo "Capturando pantallas..."
node scripts/jira_capture_screenshots.mjs

echo "Hecho. Capturas en docs/evidencias_jira/"
