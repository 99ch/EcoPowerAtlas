import { useEffect, useMemo, useState } from 'react';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from 'recharts';
import { Api } from '../api/client.js';
import { Loader } from './Loader.jsx';

const RESOURCE_TYPES = [
  { value: 'solar', label: 'Solaire' },
  { value: 'wind', label: 'Éolien' },
  { value: 'hydro', label: 'Hydro' },
  { value: 'biomass', label: 'Biomasse' },
];

export function ResourceTimeseries() {
  const [countries, setCountries] = useState([]);
  const [country, setCountry] = useState('');
  const [resourceType, setResourceType] = useState('solar');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    Api.getCountries({ page_size: 100 })
      .then((resp) => {
        if (cancelled) return;
        setCountries(resp.results);
        if (resp.results.length) {
          setCountry((prev) => prev || resp.results[0].iso3);
        }
      })
      .catch(() => null);
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Api.getResourceTimeseries({ 'country__iso3': country || undefined, resource_type: resourceType })
      .then((resp) => setData(resp.results ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [country, resourceType]);

  const chartData = useMemo(() => data.map((row) => ({ ...row, label: row.year?.toString() ?? 'n/a' })), [data]);

  return (
    <div className="timeseries-card">
      <div className="card-header">
        <h3>Séries temporelles</h3>
        <div className="filters">
          <select value={resourceType} onChange={(e) => setResourceType(e.target.value)}>
            {RESOURCE_TYPES.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
          <select value={country} onChange={(e) => setCountry(e.target.value)}>
            <option value="">Tous pays</option>
            {countries.map((item) => (
              <option key={item.iso3} value={item.iso3}>
                {item.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading && <Loader label="Agrégation en cours" />}
      {error && <p className="error">{error}</p>}
      {!loading && !error && chartData.length === 0 && <p>Aucune donnée disponible.</p>}
      {!loading && !error && chartData.length > 0 && (
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData} margin={{ top: 16, right: 32, left: 0, bottom: 8 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="label" />
              <YAxis />
              <Tooltip formatter={(value) => value?.toLocaleString('fr-FR')} labelFormatter={(label) => `Année ${label}`} />
              <Line type="monotone" dataKey="total_value" stroke="#0f9d58" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
