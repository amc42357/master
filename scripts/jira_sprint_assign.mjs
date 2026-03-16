#!/usr/bin/env node
/**
 * Crea un sprint activo en el board REHAB, asigna las issues (stories/tasks) y opcionalmente
 * las transiciona a Done/In Progress según el estado real del proyecto rehab_cv.
 * Requisitos: Jira con proyecto REHAB y issues ya inyectadas (jira_inject.mjs).
 * Uso: JIRA_USER=33moralesarmando JIRA_PASS=123456 node scripts/jira_sprint_assign.mjs
 */

const JIRA_URL = (process.env.JIRA_URL || 'http://localhost:8080').replace(/\/$/, '');
const JIRA_USER = process.env.JIRA_USER || 'admin';
const JIRA_PASS = process.env.JIRA_PASS || 'admin';
const PROJECT_KEY = process.env.JIRA_PROJECT || 'REHAB';

const auth = Buffer.from(`${JIRA_USER}:${JIRA_PASS}`).toString('base64');

async function api(path, options = {}) {
  const url = `${JIRA_URL}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Basic ${auth}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Jira ${res.status}: ${t}`);
  }
  const text = await res.text();
  return text ? JSON.parse(text) : {};
}

// Issues del sprint: REHAB-6 (US-01) .. REHAB-15 (US-10). Coinciden con el orden de jira_inject.
const SPRINT_ISSUE_KEYS = [
  'REHAB-6',  // US-01
  'REHAB-7',  // US-02
  'REHAB-8',  // US-03
  'REHAB-9',  // US-04
  'REHAB-10', // US-05
  'REHAB-11', // US-06
  'REHAB-12', // T-07
  'REHAB-13', // T-08
  'REHAB-14', // T-09
  'REHAB-15', // US-10
];

// Según rehab_cv: prototipo core (US-01..US-06), US-10, T-07 y T-09 están implementados → Done.
// T-08 (pruebas de validación) puede quedar In Progress o To Do.
const KEYS_TO_MARK_DONE = [
  'REHAB-6', 'REHAB-7', 'REHAB-8', 'REHAB-9', 'REHAB-10', 'REHAB-11', // US-01..US-06
  'REHAB-12', // T-07 protocolo
  'REHAB-14', // T-09 análisis
  'REHAB-15', // US-10 exportación
];

async function getBoardId() {
  const data = await api(`/rest/agile/1.0/board?projectKeyOrId=${PROJECT_KEY}`);
  const board = data.values?.[0];
  if (!board) throw new Error('No se encontró board para proyecto ' + PROJECT_KEY);
  return board.id;
}

async function createSprint(boardId) {
  const now = new Date();
  const start = new Date(now);
  start.setDate(start.getDate() - 14);
  const end = new Date(now);
  end.setDate(end.getDate() + 14);
  const fmt = (d) => d.toISOString().slice(0, 19).replace('T', 'T');
  const body = {
    name: 'Sprint 1 - Prototipo core',
    originBoardId: boardId,
    startDate: fmt(start),
    endDate: fmt(end),
    goal: 'Prototipo core (US-01 a US-06), exportación (US-10), protocolo (T-07), pruebas (T-08) y análisis (T-09).',
    autoStartStop: false,
    synced: false,
  };
  const sprint = await api('/rest/agile/1.0/sprint', { method: 'POST', body: JSON.stringify(body) });
  console.log('Sprint creado:', sprint.name, '(id', sprint.id + ')');
  return sprint.id;
}

async function moveIssuesToSprint(sprintId, issueKeys) {
  await api(`/rest/agile/1.0/sprint/${sprintId}/issue`, {
    method: 'POST',
    body: JSON.stringify({ issues: issueKeys }),
  });
  console.log('Issues asignadas al sprint:', issueKeys.join(', '));
}

async function startSprint(sprintId) {
  const sprint = await api(`/rest/agile/1.0/sprint/${sprintId}`);
  const body = {
    id: sprint.id,
    name: sprint.name || 'Sprint 1 - Prototipo core',
    state: 'active',
    startDate: sprint.startDate,
    endDate: sprint.endDate,
    originBoardId: sprint.originBoardId,
    goal: sprint.goal,
  };
  await api(`/rest/agile/1.0/sprint/${sprintId}`, {
    method: 'PUT',
    body: JSON.stringify(body),
  });
  console.log('Sprint activado.');
}

async function getTransitionId(issueKey, targetName) {
  const data = await api(`/rest/api/2/issue/${issueKey}/transitions`);
  const t = data.transitions?.find(
    (x) => x.name.toLowerCase() === targetName.toLowerCase() || (targetName === 'Done' && (x.to?.name?.toLowerCase() === 'done' || x.to?.name?.toLowerCase() === 'cerrado'))
  );
  if (t) return t.id;
  const toDone = data.transitions?.find((x) => x.to?.name?.toLowerCase() === 'done' || x.to?.name?.toLowerCase() === 'cerrado' || x.to?.name?.toLowerCase() === 'closed');
  return toDone?.id ?? data.transitions?.[0]?.id;
}

async function transitionIssue(issueKey, transitionId) {
  await api(`/rest/api/2/issue/${issueKey}/transitions`, {
    method: 'POST',
    body: JSON.stringify({ transition: { id: transitionId } }),
  });
}

async function main() {
  console.log('Conectando a', JIRA_URL, 'proyecto', PROJECT_KEY);

  const boardId = await getBoardId();
  console.log('Board id:', boardId);

  let sprintId = null;
  let needStart = false;
  const sprintsRes = await api(`/rest/agile/1.0/board/${boardId}/sprint?state=active,future`);
  const existing = sprintsRes.values?.find((s) => s.name.includes('Sprint 1') || s.name.includes('Prototipo') || s.state === 'active');
  if (existing) {
    sprintId = existing.id;
    needStart = existing.state === 'future';
    console.log('Usando sprint existente:', existing.name, '(id', sprintId + ')', existing.state);
  } else {
    sprintId = await createSprint(boardId);
    needStart = true;
  }
  await moveIssuesToSprint(sprintId, SPRINT_ISSUE_KEYS);
  if (needStart) await startSprint(sprintId);

  if (KEYS_TO_MARK_DONE.length > 0) {
    let transitionId = null;
    for (const key of KEYS_TO_MARK_DONE) {
      try {
        if (!transitionId) transitionId = await getTransitionId(key, 'Done');
        if (transitionId) {
          await transitionIssue(key, transitionId);
          console.log('Marcada como Done:', key);
        }
      } catch (e) {
        console.warn('No se pudo transicionar', key, ':', e.message?.slice(0, 60));
      }
    }
  }

  console.log('Listo. Board:', `${JIRA_URL}/secure/RapidBoard.jspa?projectKey=${PROJECT_KEY}`);
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
