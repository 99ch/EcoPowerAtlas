import { useEffect, useState } from 'react';
import { Api } from '../api/client.js';
import { Loader } from './Loader.jsx';

export function ClimateTimeline() {
  const [variable, setVariable] = useState('rainfall');
  const [country, setCountry] = useState('');
  const [site, setSite] = useState('');
  const [limit, setLimit] = useState(200);
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Api.getClimateTimeline({ variable, 'country__iso3': country || undefined, site: site || undefined, limit })
      .then((resp) => setData(resp.results ?? []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [variable, country, site, limit]);

  return (
    <div className="climate-card">
      <div className="card-header">
        <h3>Timeline climat</h3>
        <div className="filters">
          <input value={variable} onChange={(e) => setVariable(e.target.value)} placeholder="Variable (ex: rainfall)" />
          <input value={country} onChange={(e) => setCountry(e.target.value.toUpperCase())} placeholder="ISO3 (optionnel)" maxLength={3} />
          <input value={site} onChange={(e) => setSite(e.target.value)} placeholder="ID site" />
          <input
            type="number"
            min={50}
            max={2000}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
          />
        </div>
      </div>

      {loading && <Loader label="Séries climat" />}
      {error && <p className="error">{error}</p>}
      {!loading && !error && data.length === 0 && <p>Aucune série trouvée.</p>}

      <div className="timeline-grid">
        {data.map((series) => (
          <article key={series.id} className="timeline-card">
            <header>
              <p>{series.country_iso3}</p>
              <p>
                {series.variable} ({series.unit})
              </p>
            </header>
            <div className="timeline-points">
              {series.points?.slice(0, 30).map((point, index) => (
                <span key={`${series.id}-${index}`} title={`${point.timestamp} → ${point.value}`}>
                  {point.value}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
