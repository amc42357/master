#!/usr/bin/env bash
# Verifica: Docker activo, Jira respondiendo, datos insertados y capturas generadas.
# Uso: ./scripts/jira_verificar.sh [JIRA_PASS]
# Si pasas JIRA_PASS y Jira está listo, intenta inyectar y capturar.

set -e
JIRA_URL="${JIRA_URL:-http://localhost:8080}"
JIRA_USER="${JIRA_USER:-admin}"
JIRA_PASS="${1:-$JIRA_PASS}"
JIRA_PROJECT="${JIRA_PROJECT:-REHAB}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EVIDENCIAS="$REPO_ROOT/docs/evidencias_jira"

echo "=== 1. Docker ==="
if docker ps --format '{{.Names}}' | grep -q jira-rehab; then
  echo "OK: Contenedor jira-rehab está en ejecución."
else
  echo "NO: Contenedor Jira no está corriendo. Ejecuta: docker compose -f docker-compose.jira.yml up -d"
  exit 1
fi

echo ""
echo "=== 2. API Jira ==="
code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$JIRA_URL/rest/api/2/serverInfo" 2>/dev/null || echo "000")
if [ "$code" = "200" ] || [ "$code" = "401" ]; then
  echo "OK: Jira API responde (HTTP $code)."
  API_OK=1
else
  echo "NO: Jira API devuelve HTTP $code (503 = aún arrancando o asistente sin completar)."
  echo "    Abre $JIRA_URL en el navegador, completa el asistente y crea el proyecto REHAB."
  API_OK=0
fi

echo ""
echo "=== 3. Datos insertados ==="
if [ "$API_OK" = "1" ] && [ -n "$JIRA_PASS" ]; then
  auth=$(echo -n "$JIRA_USER:$JIRA_PASS" | base64)
  count=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 -H "Authorization: Basic $auth" "$JIRA_URL/rest/api/2/search?jql=project=${JIRA_PROJECT}&maxResults=0" 2>/dev/null || echo "0")
  if [ "$count" = "200" ]; then
    num=$(curl -s -H "Authorization: Basic $auth" "$JIRA_URL/rest/api/2/search?jql=project=${JIRA_PROJECT}&maxResults=0" 2>/dev/null | grep -o '"total":[0-9]*' | cut -d: -f2)
    if [ -n "$num" ] && [ "$num" -ge "1" ]; then
      echo "OK: Hay $num issue(s) en el proyecto $JIRA_PROJECT."
    else
      echo "AVISO: Proyecto $JIRA_PROJECT existe pero no hay issues. Ejecuta: JIRA_PASS=xxx npm run jira:inject"
    fi
  else
    echo "AVISO: No se pudo comprobar (¿proyecto $JIRA_PROJECT creado?). Crea el proyecto e inyecta con: JIRA_PASS=xxx npm run jira:inject"
  fi
else
  echo "Omiso (API no lista o JIRA_PASS no indicado). Para inyectar: JIRA_PASS=xxx npm run jira:inject"
fi

echo ""
echo "=== 4. Capturas ==="
for f in jira_board_backlog.png jira_board_sprint.png; do
  if [ -f "$EVIDENCIAS/$f" ]; then
    echo "OK: $f existe."
  else
    echo "NO: $f no encontrado en docs/evidencias_jira/."
  fi
done

if [ "$API_OK" = "1" ] && [ -n "$JIRA_PASS" ]; then
  echo ""
  echo "Para inyectar y capturar ahora: JIRA_PASS=<tu_password> ./scripts/jira_wait_inject_capture.sh"
fi
