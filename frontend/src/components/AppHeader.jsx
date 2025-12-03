import { API_BASE } from '../api/client.js';

export function AppHeader() {
  return (
    <header className="app-header">
      <div>
        <p className="eyebrow">EcoPowerAtlas</p>
        <h1>Cartographie des potentiels PHES</h1>
        <p>
          Visualisez les sites hydrauliques, séries climatiques et métriques énergétiques agrégées depuis l’API Django. L’interface est
          responsive et repose sur les endpoints `/api` récemment enrichis (résumés, séries temporelles, export).
        </p>
        <div className="header-actions">
          <a className="btn" href="/docs" target="_blank" rel="noreferrer">
            Documentation API
          </a>
          <a className="btn btn-secondary" href={API_BASE} target="_blank" rel="noreferrer">
            Explorer l’API
          </a>
        </div>
      </div>
    </header>
  );
}
