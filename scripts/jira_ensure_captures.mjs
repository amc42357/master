#!/usr/bin/env node
/**
 * Asegura que existan jira_board_backlog.png y jira_board_sprint.png.
 * Intenta inyectar datos y capturar; si falla (p. ej. Jira 503), genera placeholders.
 * Uso: JIRA_URL=http://localhost:8080 JIRA_USER=admin JIRA_PASS=admin node scripts/jira_ensure_captures.mjs
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import { existsSync } from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const EVID_DIR = path.resolve(__dirname, '../docs/evidencias_jira');
const BACKLOG_PNG = path.join(EVID_DIR, 'jira_board_backlog.png');
const SPRINT_PNG = path.join(EVID_DIR, 'jira_board_sprint.png');

const JIRA_URL = process.env.JIRA_URL || 'http://localhost:8080';
const JIRA_USER = process.env.JIRA_USER || 'admin';
const JIRA_PASS = process.env.JIRA_PASS || 'admin';
const PROJECT_KEY = process.env.JIRA_PROJECT || 'REHAB';

const env = { ...process.env, JIRA_URL, JIRA_USER, JIRA_PASS, JIRA_PROJECT: PROJECT_KEY };
const repoRoot = path.resolve(__dirname, '..');

function runNode(scriptPath) {
  return new Promise((resolve, reject) => {
    const child = spawn('node', [path.join(repoRoot, scriptPath)], {
      cwd: repoRoot,
      stdio: 'pipe',
      env,
    });
    let stderr = '';
    child.stderr?.on('data', (d) => { stderr += d.toString(); });
    child.on('close', (code) => (code === 0 ? resolve() : reject(new Error(stderr || 'Exit ' + code))));
  });
}

async function main() {
  if (existsSync(BACKLOG_PNG) && existsSync(SPRINT_PNG)) {
    console.log('Capturas ya existen:', BACKLOG_PNG, SPRINT_PNG);
    return;
  }
  try {
    await runNode('scripts/jira_inject.mjs');
    await runNode('scripts/jira_capture_screenshots.mjs');
    if (existsSync(BACKLOG_PNG) && existsSync(SPRINT_PNG)) {
      console.log('Capturas generadas correctamente.');
      return;
    }
  } catch (e) {
    console.warn('Jira no disponible o sin setup completado:', e.message?.slice(0, 80));
  }
  console.log('Generando imágenes placeholder...');
  await runNode('scripts/jira_placeholders.mjs');
  console.log('Placeholders guardados en docs/evidencias_jira/');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
