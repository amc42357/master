#!/usr/bin/env node
/**
 * Captura pantallas del backlog y board de Jira local y las guarda en docs/evidencias_jira/.
 * Requisitos: Jira en marcha, proyecto REHAB con datos (ej. tras ejecutar jira_inject.mjs).
 * Uso: JIRA_URL=http://localhost:8080 JIRA_USER=admin JIRA_PASS=admin node scripts/jira_capture_screenshots.mjs
 */

import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';
import { mkdirSync } from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, '../docs/evidencias_jira');
mkdirSync(OUT_DIR, { recursive: true });

const JIRA_URL = (process.env.JIRA_URL || 'http://localhost:8080').replace(/\/$/, '');
const JIRA_USER = process.env.JIRA_USER || 'admin';
const JIRA_PASS = process.env.JIRA_PASS || 'admin';
const PROJECT_KEY = process.env.JIRA_PROJECT || 'REHAB';

const delay = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  try {
    await page.goto(JIRA_URL + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await delay(1500);
    const userSel = page.locator('#login-form-username, #username, input[name="os_username"]').first();
    const passSel = page.locator('#login-form-password, #password, input[name="os_password"]').first();
    const submitSel = page.locator('#login-form-submit, #login, button[type="submit"]').first();
    await userSel.fill(JIRA_USER);
    await passSel.fill(JIRA_PASS);
    await submitSel.click();
    await Promise.race([
      page.waitForURL((u) => !u.pathname.includes('login'), { timeout: 25000 }),
      page.waitForSelector('#dashboard, .aui-page-header, [href*="browse"], #content', { timeout: 25000 }),
    ]).catch(() => null);
    await delay(2000);
    const url = page.url();
    if (url.includes('/login') && (await page.locator('#login-form-username, #username').count()) > 0) {
      throw new Error('Sigue en la página de login (revisa usuario/contraseña).');
    }
  } catch (e) {
    console.error('Login fallido (¿Jira listo y credenciales correctas?):', e.message);
    await browser.close();
    process.exit(1);
  }

  const boardUrl = `${JIRA_URL}/secure/RapidBoard.jspa?projectKey=${PROJECT_KEY}`;
  const jqlEncoded = `project%3D${PROJECT_KEY}%20order%20by%20rank%20asc`;
  const jqlUrls = [
    `${JIRA_URL}/issues/?jql=${jqlEncoded}`,
    `${JIRA_URL}/secure/IssueNavigator.jspa?jql=${jqlEncoded}`,
  ];

  // 1) Backlog con datos: preferir board + tab Backlog; si no hay issues visibles, usar búsqueda JQL.
  await page.goto(boardUrl, { waitUntil: 'networkidle', timeout: 25000 });
  await delay(3000);
  let backlogCaptured = false;
  const backlogTab = page.locator('a:has-text("Backlog"), button:has-text("Backlog"), [href*="backlog"], .ghx-backlog-tab').first();
  if (await backlogTab.isVisible().catch(() => false)) {
    try {
      await backlogTab.click();
      await delay(3500);
      const hasIssues = await page.locator('.ghx-issue, .ghx-backlog-group, [data-issue-key], .js-issue').count() > 0;
      if (hasIssues) {
        await page.screenshot({ path: path.join(OUT_DIR, 'jira_board_backlog.png'), fullPage: false });
        console.log('Captura: jira_board_backlog.png (tab Backlog)');
        backlogCaptured = true;
      }
    } catch (_) {}
  }
  if (!backlogCaptured) {
    for (const url of jqlUrls) {
      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
        await delay(3000);
        await page.screenshot({ path: path.join(OUT_DIR, 'jira_board_backlog.png'), fullPage: false });
        console.log('Captura: jira_board_backlog.png (lista de issues por JQL)');
        break;
      } catch (_) {}
    }
  }

  // 2) Board / Sprint: vista del tablero (epics e issues en columnas).
  await page.goto(boardUrl, { waitUntil: 'networkidle', timeout: 25000 });
  await delay(3000);
  const boardTab = page.locator('a:has-text("Board"), a:has-text("Active sprint"), a:has-text("Sprint"), .ghx-board-tab').first();
  if (await boardTab.isVisible().catch(() => false)) {
    await boardTab.click().catch(() => null);
    await delay(2500);
  }
  await page.screenshot({ path: path.join(OUT_DIR, 'jira_board_sprint.png'), fullPage: false });
  console.log('Captura: jira_board_sprint.png');

  await browser.close();
  console.log('Capturas guardadas en', OUT_DIR);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
