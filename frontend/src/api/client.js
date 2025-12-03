const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api';

const buildUrl = (path, params = {}) => {
  const url = new URL(path.replace(/^\//, ''), `${API_BASE_URL}/`);
  const cleanParams = Object.entries(params)
    .filter(([, value]) => value !== undefined && value !== null && value !== '')
    .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});
  Object.entries(cleanParams).forEach(([key, value]) => url.searchParams.append(key, value));
  return url.toString();
};

async function request(path, { params, ...options } = {}) {
  const url = buildUrl(path, params);
  const response = await fetch(url, {
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`API ${response.status}: ${detail || response.statusText}`);
  }

  const contentType = response.headers.get('content-type') ?? '';
  if (contentType.includes('application/json')) {
    return response.json();
  }
  return response.text();
}

export const Api = {
  getStats: () => request('/stats/'),
  getHydroSummary: (params) => request('/hydro-sites/summary/', { params }),
  getCountries: (params) => request('/countries/', { params }),
  getResourceTimeseries: (params) => request('/resource-metrics/timeseries/', { params }),
  getClimateTimeline: (params) => request('/climate-series/timeline/', { params }),
  enqueueSnapshot: (payload) => request('/resource-metrics/enqueue_snapshot/', {
    method: 'POST',
    body: JSON.stringify(payload ?? {}),
  }),
};

export const API_BASE = API_BASE_URL;
