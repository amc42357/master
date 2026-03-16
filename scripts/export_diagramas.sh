#!/usr/bin/env bash
# Exporta diagramas Mermaid (.mmd) a PNG y SVG para incluirlos en el documento y en la entrega.
#
# Uso: ./scripts/export_diagramas.sh   (ejecutar desde la raíz del proyecto)
# Alternativa: npm run export-diagramas
#
# Requiere: Node.js y mermaid-cli (npm install en el proyecto o global: npm install -g @mermaid-js/mermaid-cli).
# Los diagramas también pueden exportarse copiando el código de proyecto.md o diagrams/*.mmd en https://mermaid.live
#
# Salida: diagrams/*.png y diagrams/*.svg

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DIAGRAMS_DIR="$ROOT_DIR/diagrams"
cd "$ROOT_DIR"

if [[ ! -d "$DIAGRAMS_DIR" ]]; then
  echo "No existe la carpeta diagrams/. Nada que exportar."
  exit 0
fi

# Preferir mmdc local (node_modules); luego global (PATH); luego npx
MMDC=""
if [[ -x "$ROOT_DIR/node_modules/.bin/mmdc" ]]; then
  MMDC="$ROOT_DIR/node_modules/.bin/mmdc"
elif command -v mmdc &>/dev/null; then
  MMDC="mmdc"
elif command -v npx &>/dev/null; then
  MMDC="npx -y @mermaid-js/mermaid-cli -- mmdc"
else
  echo "Advertencia: no se encontró mmdc ni npx. Ejecute en la raíz: npm install"
  echo "O instale Node.js y mermaid-cli: npm install -g @mermaid-js/mermaid-cli"
  echo "También puede exportar copiando el código Mermaid de proyecto.md o diagrams/*.mmd en https://mermaid.live"
  exit 1
fi

echo "Exportando diagramas Mermaid a PNG y SVG..."
for mmd in "$DIAGRAMS_DIR"/*.mmd; do
  [[ -f "$mmd" ]] || continue
  base=$(basename "$mmd" .mmd)
  echo "  $base.mmd -> $base.png, $base.svg"
  $MMDC -i "$mmd" -o "$DIAGRAMS_DIR/$base.png" -b white
  $MMDC -i "$mmd" -o "$DIAGRAMS_DIR/$base.svg" -b white
done

echo "Listo. Imágenes en: $DIAGRAMS_DIR/"
