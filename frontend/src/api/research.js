const API_BASE = '/api';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function createResearchRun(payload) {
  const res = await fetch(`${API_BASE}/research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.message || errData.error || `HTTP error ${res.status}`);
  }
  return res.json();
}

export async function fetchResearchRuns(limit = 20, offset = 0) {
  const res = await fetch(`${API_BASE}/research?limit=${limit}&offset=${offset}`);
  if (!res.ok) throw new Error(`Failed to fetch research runs: ${res.statusText}`);
  return res.json();
}

export async function fetchResearchRun(researchId) {
  const res = await fetch(`${API_BASE}/research/${researchId}`);
  if (!res.ok) throw new Error(`Failed to fetch research run: ${res.statusText}`);
  return res.json();
}

export async function fetchResearchEvents(researchId) {
  const res = await fetch(`${API_BASE}/research/${researchId}/events`);
  if (!res.ok) throw new Error(`Failed to fetch research events: ${res.statusText}`);
  return res.json();
}

export function subscribeToResearchEvents(researchId, onEvent, onError) {
  const eventSource = new EventSource(`${API_BASE}/research/${researchId}/stream`);

  const eventTypes = [
    'research_started',
    'plan_created',
    'search_started',
    'evidence_found',
    'research_completed',
    'done',
    'error'
  ];

  eventTypes.forEach((type) => {
    eventSource.addEventListener(type, (event) => {
      try {
        const parsed = JSON.parse(event.data);
        onEvent({ type, data: parsed });
        if (type === 'done' || type === 'error') {
          eventSource.close();
        }
      } catch (err) {
        console.error('Error parsing SSE event data:', err);
      }
    });
  });

  eventSource.onerror = (err) => {
    if (onError) onError(err);
    eventSource.close();
  };

  return () => {
    eventSource.close();
  };
}
