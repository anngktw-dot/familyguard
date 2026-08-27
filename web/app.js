const params = new URLSearchParams(window.location.search);
const configuredApi = params.get('api');

if (configuredApi) {
  localStorage.setItem('familyguard.api', configuredApi);
}

const API = (configuredApi || localStorage.getItem('familyguard.api') || 'http://127.0.0.1:8000')
  .replace(/\/$/, '');
const CHILD_ID = 1;

function formatMinutes(minutes) {
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return hours ? `${hours}h ${rest}m` : `${rest}m`;
}

function renderApps(apps) {
  const container = document.getElementById('apps');
  container.replaceChildren();

  for (const app of apps) {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = app;
    container.appendChild(chip);
  }
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API}${path}`, options);
  if (!response.ok) {
    let detail = 'Request failed';
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch (_) {
      // Keep the generic message when the response has no JSON body.
    }
    throw new Error(detail);
  }
  return response.json();
}

async function loadParentDashboard() {
  const child = await apiRequest(`/children/${CHILD_ID}`);

  document.getElementById('name').textContent = child.name;
  document.getElementById('status').textContent = child.status;
  document.getElementById('location').textContent = child.location_label;
  document.getElementById('battery').textContent = `${child.battery_percent}%`;
  document.getElementById('screenTime').textContent = formatMinutes(child.screen_time_minutes);
  document.getElementById('lastCheckIn').textContent = new Date(child.last_check_in).toLocaleString();
  renderApps(child.top_apps);
}

async function sendCheckIn() {
  const status = document.getElementById('statusInput').value.trim();
  const locationLabel = document.getElementById('locationInput').value.trim() || 'Not shared';
  const batteryPercent = Number(document.getElementById('batteryInput').value);
  const result = document.getElementById('result');
  const button = document.getElementById('sendCheckIn');

  if (!status) {
    result.textContent = 'Add a status before sending your check-in.';
    return;
  }

  button.disabled = true;
  result.textContent = 'Sending…';

  try {
    await apiRequest(`/children/${CHILD_ID}/check-in`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        status,
        location_label: locationLabel,
        battery_percent: batteryPercent,
      }),
    });
    result.textContent = 'Check-in sent successfully.';
  } finally {
    button.disabled = false;
  }
}

const page = document.body.dataset.page;

if (page === 'parent') {
  loadParentDashboard().catch((error) => {
    document.getElementById('status').textContent = error.message;
  });

  document.getElementById('refresh').addEventListener('click', () => {
    loadParentDashboard().catch((error) => {
      document.getElementById('status').textContent = error.message;
    });
  });
}

if (page === 'child') {
  const battery = document.getElementById('batteryInput');
  const batteryValue = document.getElementById('batteryValue');

  battery.addEventListener('input', () => {
    batteryValue.textContent = `${battery.value}%`;
  });

  document.getElementById('sendCheckIn').addEventListener('click', () => {
    sendCheckIn().catch((error) => {
      document.getElementById('result').textContent = error.message;
    });
  });
}
