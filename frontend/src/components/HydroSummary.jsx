import { useEffect, useState } from 'react';
import { Api } from '../api/client.js';
import { Loader } from './Loader.jsx';

export function HydroSummary() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Api.getHydroSummary()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Agrégats PHES" />;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="hydro-summary">
      <div>
        <p className="stat-label">Total sites</p>
        <p className="stat-value">{data.total_sites}</p>
      </div>
      <div>
        <p className="stat-label">Capacité stockage (MWh)</p>
        <p className="stat-value">{Math.round(data.total_storage_mwh)}</p>
      </div>
      <div>
        <p className="stat-label">Capacité turbine (MW)</p>
        <p className="stat-value">{Math.round(data.total_capacity_mw)}</p>
      </div>
      <div>
        <p className="stat-label">Top pays</p>
        <ol>
          {data.top_countries.map((country) => (
            <li key={country.country__iso3}>
              {country.country__name} ({country.site_count})
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
