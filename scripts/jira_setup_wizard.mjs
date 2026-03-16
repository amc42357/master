#!/usr/bin/env node
/**
 * Intenta completar el asistente de primera configuración de Jira y crear el proyecto REHAB.
 * Después se pueden ejecutar jira_inject.mjs y jira_capture_screenshots.mjs.
 * Uso: JIRA_URL=http://localhost:8080 JIRA_USER=admin JIRA_PASS=admin node scripts/jira_setup_wizard.mjs
 */

import { chromium } from 'playwright';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..');

const JIRA_URL = (process.env.JIRA_URL || 'http://localhost:8080').replace(/\/$/, '');
const JIRA_USER = process.env.JIRA_USER || 'admin';
const JIRA_PASS = process.env.JIRA_PASS || 'admin';
const PROJECT_KEY = process.env.JIRA_PROJECT || 'REHAB';

const delay = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.setDefaultTimeout(20000);

  try {
    await page.goto(JIRA_URL + '/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await delay(3000);

    const url = page.url();
    const content = await page.content();

    // ¿Estamos en el asistente de configuración?
    if (url.includes('Setup') || url.includes('setup') || content.includes('Set up Jira') || content.includes('Welcome to Jira')) {
      console.log('Detectado asistente de configuración. Intentando completar...');

      // Paso: idioma (siguiente)
      const nextBtn = page.locator('button:has-text("Next"), button:has-text("Siguiente"), input[value="Next"], #next, .button-panel-button').first();
      if (await nextBtn.isVisible().catch(() => false)) {
        await nextBtn.click();
        await delay(2000);
      }

      // Licencia: generar evaluación
      const licenseBtn = page.locator('button:has-text("Generate"), a:has-text("Generate"), *:has-text("evaluation license")').first();
      if (await licenseBtn.isVisible().catch(() => false)) {
        await licenseBtn.click();
        await delay(2000);
      }
      const next2 = page.locator('button:has-text("Next"), button:has-text("Siguiente"), #next').first();
      if (await next2.isVisible().catch(() => false)) {
        await next2.click();
        await delay(2000);
      }

      // Cuenta de administrador
      const userInput = page.locator('#jira-setup-username, #username, input[name="username"], input[name="jira-setup-username"]').first();
      const passInput = page.locator('#jira-setup-password, #password, input[name="password"], input[type="password"]').first();
      if (await userInput.isVisible().catch(() => false)) {
        await userInput.fill(JIRA_USER);
        await passInput.fill(JIRA_PASS);
        await delay(500);
        const submitSetup = page.locator('button:has-text("Next"), button:has-text("Submit"), button:has-text("Confirm"), #next, #submit').first();
        await submitSetup.click();
        await delay(5000);
      }

      // Finalizar asistente
      const finishBtn = page.locator('button:has-text("Finish"), button:has-text("Close"), #finish, a:has-text("Finish")').first();
      if (await finishBtn.isVisible().catch(() => false)) {
        await finishBtn.click();
        await delay(5000);
      }
    }

    // Buscar formulario de login por si ya pasamos el asistente
    const loginUser = page.locator('#login-form-username, #username, input[name="os_username"]').first();
    if (await loginUser.isVisible().catch(() => false)) {
      await loginUser.fill(JIRA_USER);
      await page.locator('#login-form-password, #password, input[name="os_password"]').first().fill(JIRA_PASS);
      await page.locator('#login-form-submit, #login, button[type="submit"]').first().click();
      await page.waitForURL((u) => !u.pathname.includes('login'), { timeout: 15000 }).catch(() => null);
      await delay(3000);
    }

    // Crear proyecto REHAB si no existe: ir a crear proyecto (Scrum)
    await page.goto(JIRA_URL + '/secure/CreateProject.jspa', { waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => null);
    await delay(2000);
    const projectKeyInput = page.locator('#projectKey, input[name="projectKey"], #key').first();
    if (await projectKeyInput.isVisible().catch(() => false)) {
      await projectKeyInput.fill(PROJECT_KEY);
      const nameInput = page.locator('#projectName, input[name="name"]').first();
      if (await nameInput.isVisible().catch(() => false)) await nameInput.fill('Rehabilitación motriz');
      const submitProject = page.locator('button:has-text("Submit"), #project-create-submit, input[type="submit"]').first();
      if (await submitProject.isVisible().catch(() => false)) {
        await submitProject.click();
        await delay(5000);
      }
    }

    await browser.close();
  } catch (e) {
    console.warn('Setup wizard:', e.message);
    await browser.close();
  }

  // Esperar a que la API responda (hasta ~5 min)
  let apiReady = false;
  console.log('Esperando a que la API de Jira esté disponible...');
  for (let i = 0; i < 60; i++) {
    try {
      const res = await fetch(JIRA_URL + '/rest/api/2/serverInfo', { method: 'GET' });
      const status = res.status || 503;
      if (status === 200 || status === 401) {
        console.log('API lista (HTTP ' + status + ').');
        apiReady = true;
        break;
      }
    } catch (_) {}
    await delay(5000);
  }

  const env = { ...process.env, JIRA_URL, JIRA_USER, JIRA_PASS, JIRA_PROJECT: PROJECT_KEY };
  let injectOk = false;
  let captureOk = false;

  if (apiReady) {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        console.log('Inyectando épicas e issues (intento ' + attempt + '/3)...');
        await runNode('scripts/jira_inject.mjs', env);
        injectOk = true;
        break;
      } catch (e) {
        console.warn('Inyección fallida:', e.message);
        await delay(15000);
      }
    }
    if (injectOk) await delay(2000);
    try {
      console.log('Generando capturas...');
      await runNode('scripts/jira_capture_screenshots.mjs', env);
      captureOk = true;
    } catch (e) {
      console.warn('Capturas fallidas:', e.message);
    }
  }

  if (!captureOk) {
    console.log('Generando imágenes placeholder (complete el asistente en ' + JIRA_URL + ' y vuelva a ejecutar para capturas reales).');
    await runNode('scripts/jira_placeholders.mjs', env);
  }
}

function runNode(scriptPath, env = process.env) {
  return new Promise((resolve, reject) => {
    const child = spawn('node', [path.join(REPO_ROOT, scriptPath)], {
      cwd: REPO_ROOT,
      stdio: 'inherit',
      env: { ...process.env, ...env },
    });
    child.on('close', (code) => (code === 0 ? resolve() : reject(new Error('Exit ' + code))));
  });
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
