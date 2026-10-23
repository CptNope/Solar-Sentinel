'use strict';
const $ = (selector, root = document) => root.querySelector(selector);
let token = '';
let state = null;
let reportSignature = '';
let refreshing = false;
let toastTimer;
let requestId = null;
function el(tag, text, className) {
  const item = document.createElement(tag);
  if (text !== undefined) item.textContent = text;
  if (className) item.className = className;
  return item;
}
function toast(message) {
  $('#toast').textContent = message;
  $('#toast').hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { $('#toast').hidden = true; }, 4500);
}
function showDialog(id) {
  const dialog = $(id);
  $('.form-error', dialog).textContent = '';
  dialog.showModal();
}
async function api(path, method = 'GET', body) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(path, {method, cache: 'no-store', signal: controller.signal,
      headers: {'Content-Type': 'application/json', ...(token ? {Authorization: `Bearer ${token}`} : {})},
      ...(body === undefined ? {} : {body: JSON.stringify(body)})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The request could not be completed.');
    return data;
  } catch (error) {
    if (error.name === 'AbortError' || error instanceof TypeError) {
      throw new Error('Cannot reach the server. Your input is preserved; reconnect and try again.');
    }
    throw error;
  } finally { clearTimeout(timer); }
}
function age(seconds) {
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}
function renderNodes() {
  const nodes = state.nodes;
  $('#node-count').textContent = nodes.length;
  $('#node-badge').textContent = nodes.length;
  $('#node-detail').textContent = nodes.length ? 'Reporting to this field server' : 'Ready for your first check-in';
  $('#online-count').textContent = nodes.filter(n => n.status === 'online').length;
  $('#attention-count').textContent = nodes.filter(n => n.status !== 'online' || (n.battery !== null && n.battery <= 20)).length;
  $('#report-count').textContent = state.open_reports;
  $('#nodes-empty').hidden = nodes.length > 0;
  const rows = nodes.map(node => {
    const row = el('tr');
    const name = el('td');
    name.append(el('div', node.name, 'node-name'), el('small', node.id));
    const status = el('td'); status.append(el('span', node.status, `status ${node.status}`));
    const battery = el('td');
    if (node.battery === null) battery.textContent = '—';
    else {
      const wrap = el('div', undefined, 'battery');
      const meter = el('meter'); meter.min = 0; meter.max = 100; meter.low = 20; meter.high = 40; meter.optimum = 100; meter.value = node.battery;
      meter.setAttribute('aria-label', `${node.name} battery`);
      wrap.append(meter, el('span', `${node.battery}%`, node.battery <= 20 ? 'amber' : ''));
      battery.append(wrap);
    }
    const voltage = el('td', node.voltage === null ? '—' : `${node.voltage.toFixed(2)} V`);
    const position = el('td', node.latitude === null ? '—' : `${node.latitude.toFixed(4)}, ${node.longitude.toFixed(4)}`, 'dim');
    const seen = el('td', age(node.age_seconds), 'dim');
    seen.title = new Date(node.last_seen * 1000).toLocaleString();
    if (node.status !== 'online') { battery.append(el('small', 'Last reported')); voltage.append(el('small', 'Last reported')); }
    row.append(name, status, battery, voltage, position, seen);
    return row;
  });
  $('#node-rows').replaceChildren(...rows);
}
function renderReports(force = false) {
  if (!state) return;
  const filter = $('#report-filter').value;
  const signature = JSON.stringify([state.reports, filter, Boolean(token)]);
  if (!force && signature === reportSignature) return;
  reportSignature = signature;
  const reports = state.reports.filter(r => filter === 'all' || (filter === 'open' && !r.resolved) || (filter === 'resolved' && r.resolved) || (filter === 'urgent' && r.priority === 'urgent'));
  const list = $('#report-list');
  list.replaceChildren();
  if (!reports.length) {
    const empty = el('div', undefined, 'empty');
    empty.append(el('h3', filter === 'all' ? 'A quiet start' : 'No matching reports'), el('p', 'New reports and field updates will appear here.'));
    list.append(empty);
  }
  for (const report of reports) {
    const article = el('article', undefined, 'report');
    const head = el('div', undefined, 'report-head');
    const timestamp = el('time', new Date(report.created * 1000).toLocaleString([], {month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'}));
    timestamp.dateTime = new Date(report.created * 1000).toISOString();
    head.append(el('strong', report.author), el('span', report.resolved ? 'Resolved' : report.priority, `priority ${report.resolved ? 'resolved' : report.priority}`), timestamp);
    const bottom = el('div', undefined, 'report-bottom');
    const action = el('button', report.resolved ? 'Reopen report' : 'Mark resolved');
    action.type = 'button';
    action.addEventListener('click', async () => {
      if (!token) { showDialog('#access-dialog'); return; }
      action.disabled = true;
      try { await api(`/api/reports/${report.id}`, 'PATCH', {resolved: !report.resolved}); toast(report.resolved ? 'Report reopened.' : 'Report resolved.'); await refresh(); }
      catch (error) { toast(error.message); }
      finally { action.disabled = false; }
    });
    bottom.append(el('span', `REPORT ${String(report.id).padStart(3, '0')}`), action);
    article.append(head, el('p', report.message), bottom);
    list.append(article);
  }
}
async function refresh() {
  if (refreshing) return;
  refreshing = true;
  try {
    state = await api('/api/state');
    $('#connection').textContent = 'Server connected';
    $('#connection').className = 'connection ok';
    $('#network-banner').hidden = true;
    $('#demo-banner').hidden = !state.demo;
    $('#updated').textContent = `Synced ${new Date(state.server_time * 1000).toLocaleTimeString()}`;
    renderNodes(); renderReports();
  } catch (_) {
    $('#connection').textContent = 'Server unavailable';
    $('#connection').className = 'connection bad';
    $('#network-banner').hidden = false;
  } finally { refreshing = false; }
}
const reportForm = $('#report-form');
function saveDraft() {
  requestId = null;
  try { localStorage.setItem('sentinel-report-draft', JSON.stringify(Object.fromEntries(new FormData(reportForm)))); }
  catch (_) { toast('Draft storage is unavailable. Keep this page open until you submit.'); }
}
try {
  const draft = JSON.parse(localStorage.getItem('sentinel-report-draft') || 'null');
  if (draft) for (const key of ['author', 'message', 'priority']) if (typeof draft[key] === 'string') reportForm.elements[key].value = draft[key];
  if (draft && typeof draft.request_id === 'string') requestId = draft.request_id;
} catch (_) { /* The form remains usable if browser storage is disabled. */ }
reportForm.addEventListener('input', saveDraft);
reportForm.addEventListener('submit', async event => {
  event.preventDefault();
  const errorBox = $('.form-error', reportForm);
  if (!token) { errorBox.textContent = 'Close this form and enter Operator access first. Your draft is saved.'; return; }
  const button = $('button[type=submit]', reportForm);
  const data = Object.fromEntries(new FormData(reportForm));
  if (!requestId) requestId = Array.from(crypto.getRandomValues(new Uint8Array(16)), b => b.toString(16).padStart(2, '0')).join('');
  data.request_id = requestId;
  try { localStorage.setItem('sentinel-report-draft', JSON.stringify(data)); } catch (_) {}
  button.disabled = true; errorBox.textContent = '';
  try {
    await api('/api/reports', 'POST', data);
    reportForm.reset(); requestId = null;
    try { localStorage.removeItem('sentinel-report-draft'); } catch (_) {}
    $('#report-dialog').close(); toast('Field report saved.'); await refresh();
  } catch (error) { errorBox.textContent = error.message; }
  finally { button.disabled = false; }
});
$('#node-form').addEventListener('submit', async event => {
  event.preventDefault();
  const form = event.target;
  const errorBox = $('.form-error', form);
  if (!token) { errorBox.textContent = 'Close this form and enter Operator access first.'; return; }
  const data = Object.fromEntries(new FormData(form));
  for (const key of ['battery', 'voltage', 'latitude', 'longitude']) data[key] = data[key] === '' ? null : Number(data[key]);
  const button = $('button[type=submit]', form); button.disabled = true; errorBox.textContent = '';
  try { await api('/api/nodes', 'POST', data); form.reset(); $('#node-dialog').close(); toast('Node checked in.'); await refresh(); }
  catch (error) { errorBox.textContent = error.message; }
  finally { button.disabled = false; }
});
$('#access-form').addEventListener('submit', async event => {
  event.preventDefault();
  const form = event.target;
  token = form.elements.token.value.trim();
  try {
    await api('/api/access', 'POST', {});
    form.reset(); $('#access-button').textContent = 'Operator connected'; $('#access-dialog').close(); toast('Operator access enabled.'); renderReports(true);
  } catch (error) { token = ''; $('#access-button').textContent = 'Operator access'; $('.form-error', form).textContent = error.message; }
});
$('#lock').addEventListener('click', () => { token = ''; $('#access-form').reset(); $('#access-button').textContent = 'Operator access'; $('#access-dialog').close(); toast('Operator access cleared.'); });
$('#new-report').addEventListener('click', () => showDialog('#report-dialog'));
$('#check-in-button').addEventListener('click', () => showDialog('#node-dialog'));
$('#access-button').addEventListener('click', () => showDialog('#access-dialog'));
$('#report-filter').addEventListener('change', () => renderReports(true));
document.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
window.addEventListener('online', refresh);
document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
refresh();
setInterval(() => { if (!document.hidden) refresh(); }, 10000);
