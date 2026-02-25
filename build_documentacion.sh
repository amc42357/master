#!/usr/bin/env bash
# Convierte la documentación Markdown (proyecto + anexos) a PDF,
# crea la carpeta de salida y la comprime en un ZIP.
#
# Uso: ./build_documentacion.sh   (ejecutar desde la raíz del proyecto)
#
# Requiere: pandoc (brew install pandoc), TeX Live o MacTeX (xelatex/lualatex).
# Salida: carpeta entrega_pdf/ y ZIP documentacion_seminario.zip.
# Formato: plantilla UNIR (márgenes 3/2/2.5 cm, Calibri 12pt, interlineado 1.5).
# Si Calibri no está disponible, cambia mainfont en PANDOC_OPTS a "DejaVu Sans" o "Helvetica".

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

OUT_DIR="entrega_pdf"
ZIP_NAME="documentacion_seminario.zip"

# xelatex necesario para caracteres Unicode (≤, ≥). Latin Modern viene con TeX Live
PDF_ENGINE=""
for engine in xelatex lualatex pdflatex; do
  if command -v "$engine" &>/dev/null; then
    PDF_ENGINE="$engine"
    break
  fi
done

if [[ -z "$PDF_ENGINE" ]]; then
  echo "Error: no se encontró xelatex, lualatex ni pdflatex. Instala TeX Live o MacTeX."
  exit 1
fi

if ! command -v pandoc &>/dev/null; then
  echo "Error: pandoc no está instalado. Instálalo con: brew install pandoc"
  exit 1
fi

echo "Usando motor PDF: $PDF_ENGINE (formato UNIR: márgenes 3/2/2.5 cm, Calibri 12pt)"
echo "Creando carpeta $OUT_DIR..."
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# Opciones base para todos los PDF
PANDOC_BASE=(
  --pdf-engine="$PDF_ENGINE"
  -V lang=es
  -V documentclass=article
  -V papersize=a4
  -V geometry="left=3cm,right=2cm,top=2.5cm,bottom=2.5cm"
  -V fontsize=12pt
  -V linestretch=1.5
  -V mainfont="Helvetica"
  --standalone
)

# Proyecto principal: portada UNIR + mejoras de saltos de página
echo "Convirtiendo proyecto.md -> proyecto.pdf"
pandoc "proyecto.md" -o "$OUT_DIR/proyecto.pdf" "${PANDOC_BASE[@]}" \
  -H pandoc-header.tex \
  -B pandoc-title.tex

# Anexos (sin portada especial)
echo "Convirtiendo anexos..."
for f in anexos/*.md; do
  [[ -f "$f" ]] || continue
  name=$(basename "$f" .md)
  echo "  $f -> ${name}.pdf"
  pandoc "$f" -o "$OUT_DIR/${name}.pdf" "${PANDOC_BASE[@]}" \
    --resource-path="anexos:."
done

# ZIP con la carpeta
echo "Generando $ZIP_NAME..."
rm -f "$ZIP_NAME"
zip -r "$ZIP_NAME" "$OUT_DIR"

echo ""
echo "Listo. PDFs en: $OUT_DIR/"
echo "ZIP generado: $ZIP_NAME"
