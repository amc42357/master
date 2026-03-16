#!/usr/bin/env node
/**
 * Inyecta épicas, historias y tareas en Jira local vía REST API.
 * Requisitos: Jira en http://localhost:8080, asistente completado, proyecto REHAB creado (Scrum).
 * Uso: JIRA_URL=http://localhost:8080 JIRA_USER=admin JIRA_PASS=admin node scripts/jira_inject.mjs
 */

const JIRA_URL = (process.env.JIRA_URL || 'http://localhost:8080').replace(/\/$/, '');
const JIRA_USER = process.env.JIRA_USER || 'admin';
const JIRA_PASS = process.env.JIRA_PASS || 'admin';
const PROJECT_KEY = process.env.JIRA_PROJECT || 'REHAB';

const auth = Buffer.from(`${JIRA_USER}:${JIRA_PASS}`).toString('base64');

async function jira(path, options = {}) {
  const url = `${JIRA_URL}/rest/api/2${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Jira ${res.status}: ${t}`);
  }
  return res.json();
}

async function ensureProjectExists() {
  const url = `${JIRA_URL}/rest/api/2/project/${PROJECT_KEY}`;
  const res = await fetch(url, {
    headers: { 'Authorization': `Basic ${auth}` },
  });
  if (res.ok) {
    console.log('Proyecto', PROJECT_KEY, 'ya existe.');
    return;
  }
  if (res.status !== 404) {
    const t = await res.text();
    throw new Error(`Jira ${res.status}: ${t}`);
  }
  console.log('Creando proyecto', PROJECT_KEY, '(Scrum)...');
  const body = {
    key: PROJECT_KEY,
    name: 'Rehabilitación motriz asistida por CV',
    projectTypeKey: 'software',
    projectTemplateKey: 'com.pyxis.greenhopper.jira:gh-scrum-template',
    lead: JIRA_USER,
    assigneeType: 'PROJECT_LEAD',
  };
  await jira('/project', { method: 'POST', body: JSON.stringify(body) });
  console.log('Proyecto', PROJECT_KEY, 'creado.');
}

// Jira 9 deprecó createmeta; usamos campos conocidos del template Scrum.
const EPIC_NAME_FIELD = 'customfield_10105'; // "Epic Name" en Scrum

async function createIssue(fields) {
  const body = { fields: { project: { key: PROJECT_KEY }, ...fields } };
  const out = await jira('/issue', { method: 'POST', body: JSON.stringify(body) });
  return out.key;
}

const EPICS = [
  { summary: 'E1: Prototipo core', epicName: 'E1 Prototipo core', description: 'Entorno, captura, pose, ángulo, conteo, feedback. Contiene US-01 a US-06.' },
  { summary: 'E2: Validación experimental', epicName: 'E2 Validación experimental', description: 'Protocolo, pruebas y análisis. Contiene T-07, T-08, T-09.' },
  { summary: 'E3: Entrega y documentación', epicName: 'E3 Entrega y documentación', description: 'Entrega y documentación. Contiene US-10.' },
];

const ISSUES = [
  { summary: 'US-01 Configuración del entorno', description: '(1) venv creado; (2) requirements.txt con opencv-python, mediapipe, numpy; (3) script de prueba que importa librerías; (4) proyecto en Git con /src, /docs, /data.', type: 'Story', epicIndex: 0, storyPoints: 1 },
  { summary: 'US-02 Captura de video en tiempo real', description: '(1) Captura con OpenCV desde cámara por defecto; (2) ventana con video en vivo; (3) cierre correcto; (4) resolución 720p o superior.', type: 'Story', epicIndex: 0, storyPoints: 2 },
  { summary: 'US-03 Visualización del esqueleto', description: '(1) MediaPipe Pose integrado; (2) dibujo de landmarks y conexiones; (3) hombro, codo y cadera visibles; (4) integrado con ventana de video US-02.', type: 'Story', epicIndex: 0, storyPoints: 3 },
  { summary: 'US-04 Cálculo y visualización de ángulo', description: '(1) Ángulo de abducción (cadera-hombro-codo); (2) valor en grados visible; (3) actualización frame a frame; (4) código documentado.', type: 'Story', epicIndex: 0, storyPoints: 5 },
  { summary: 'US-05 Conteo automático de repeticiones', description: '(1) Máquina de estados subida/bajada; (2) umbrales configurables (ej. 60°); (3) contador visible; (4) sin falsos positivos evidentes.', type: 'Story', epicIndex: 0, storyPoints: 5 },
  { summary: 'US-06 Retroalimentación de corrección', description: '(1) Mensajes según reglas; (2) criterios por umbrales; (3) mensajes en zona dedicada; (4) integración con conteo.', type: 'Story', epicIndex: 0, storyPoints: 8 },
  { summary: 'T-07 Diseño del protocolo de validación', description: '(1) Documento con hipótesis, métricas y criterios; (2) fases: reclutamiento, configuración, ejecución, análisis; (3) materiales y revisión.', type: 'Task', epicIndex: 1, storyPoints: 3 },
  { summary: 'T-08 Pruebas de validación y datos', description: '(1) Al menos 5 sujetos; (2) consentimiento firmado; (3) 3×10 repeticiones con goniómetro y grabación; (4) logs CSV y backup.', type: 'Task', epicIndex: 1, storyPoints: 8 },
  { summary: 'T-09 Análisis y gráficos', description: '(1) Script que calcula MAE, precisión y latencia; (2) gráficos y tablas; (3) informe con resultados y limitaciones.', type: 'Task', epicIndex: 1, storyPoints: 5 },
  { summary: 'US-10 Exportación de reportes', description: '(1) Exportación a CSV; (2) opción PDF si hay tiempo; (3) archivos en carpeta local; (4) documentado en README.', type: 'Story', epicIndex: 2, storyPoints: 5 },
];

async function main() {
  console.log('Conectando a', JIRA_URL, 'proyecto', PROJECT_KEY);
  await ensureProjectExists();

  const epicKeys = [];
  for (const e of EPICS) {
    const key = await createIssue({
      summary: e.summary,
      description: e.description,
      issuetype: { name: 'Epic' },
      [EPIC_NAME_FIELD]: e.epicName,
    });
    epicKeys.push(key);
    console.log('Creada épica:', key, e.summary);
  }

  for (const i of ISSUES) {
    const key = await createIssue({
      summary: i.summary,
      description: i.description,
      issuetype: { name: i.type },
    });
    console.log('Creada issue:', key, i.summary);
  }

  console.log('Listo. Abre', `${JIRA_URL}/browse/${PROJECT_KEY}`, 'para ver el backlog.');
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
