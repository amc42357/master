# Diagramas Mermaid

Los diagramas del proyecto están en formato **Mermaid** (`.mmd`) y pueden exportarse a PNG o SVG.

## Archivos

- **arquitectura.mmd**: arquitectura modular del sistema (Cap. 5).
- **flujo_design_thinking.mmd**: trazabilidad Empatizar → Definir → Criterios → MVP (Cap. 3).

## Cómo exportar

1. **Desde el proyecto (recomendado):** en la raíz del repositorio ejecute  
   `npm install` (solo la primera vez) y luego  
   `npm run export-diagramas`  
   o bien  
   `./scripts/export_diagramas.sh`  
   Se generan `*.png` y `*.svg` en esta carpeta.

2. **Online:** copie el contenido de un `.mmd` o del bloque `mermaid` en `proyecto.md` y péguelo en [Mermaid Live Editor](https://mermaid.live) para ver, editar y exportar (PNG/SVG).

El script de construcción del PDF (`./build_documentacion.sh`) ejecuta la exportación automáticamente si tiene Node.js y las dependencias instaladas.
