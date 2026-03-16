#!/usr/bin/env node
/**
 * Genera imágenes placeholder para las capturas de Jira cuando el asistente no está completado.
 * Escribe jira_board_backlog.png y jira_board_sprint.png en docs/evidencias_jira/.
 * Uso: node scripts/jira_placeholders.mjs
 */

import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';
import { mkdirSync } from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, '../docs/evidencias_jira');
mkdirSync(OUT_DIR, { recursive: true });

const JIRA_URL = process.env.JIRA_URL || 'http://localhost:8080';

const HTML = (titulo) => `<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; }
  body { font-family: system-ui, sans-serif; margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f4f5f7; color: #172b4d; }
  .card { background: #fff; border-radius: 8px; padding: 2rem; max-width: 560px; box-shadow: 0 2px 8px rgba(0,0,0,.1); }
  h1 { margin: 0 0 1rem; font-size: 1.25rem; }
  ol { margin: 0; padding-left: 1.25rem; line-height: 1.6; }
  a { color: #0052cc; }
</style></head><body>
  <div class="card">
    <h1>${titulo}</h1>
    <p>Para generar capturas reales:</p>
    <ol>
      <li>Complete el asistente en <a href="${JIRA_URL}">${JIRA_URL}</a></li>
      <li>Cree el proyecto <strong>REHAB</strong> (Scrum)</li>
      <li>Ejecute: <code>npm run jira:inject</code> y <code>npm run jira:capture</code></li>
    </ol>
  </div>
</body></html>`;

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const names = [
    { name: 'jira_board_backlog', title: 'Backlog (placeholder)' },
    { name: 'jira_board_sprint', title: 'Board / Sprint (placeholder)' },
  ];
  for (const { name, title } of names) {
    await page.setContent(HTML(title), { waitUntil: 'domcontentloaded' });
    await page.screenshot({ path: path.join(OUT_DIR, `${name}.png`), fullPage: false });
    console.log('Generado:', name + '.png');
  }
  await browser.close();
  console.log('Placeholders guardados en', OUT_DIR);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
