import { useEffect, useState } from 'react';
import { Api } from '../api/client.js';
import { Loader } from './Loader.jsx';

const defaultStats = { countries: [], resources: [], dataset_count: 0 };

export function StatsPanel() {
  const [stats, setStats] = useState(defaultStats);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Api.getStats()
      .then(setStats)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Chargement des statistiques" />;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="stats-panel">
      <div className="stat-card">
        <p className="stat-label">Jeux de données</p>
        <p className="stat-value">{stats.dataset_count}</p>
      </div>
      <div className="stat-card">
        <p className="stat-label">Top pays (sites)</p>
        <ul>
          {stats.countries.map((country) => (
            <li key={country.iso3}>
              <strong>{country.name}</strong> • {country.site_count} site(s)
            </li>
          ))}
        </ul>
      </div>
      <div className="stat-card">
        <p className="stat-label">Ressources suivies</p>
        <ul>
          {stats.resources.map((resource) => (
            <li key={resource.resource_type}>
              {resource.resource_type} : {resource.total?.toLocaleString('fr-FR')} ({resource.metrics} mesures)
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
