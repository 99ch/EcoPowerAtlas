import { useState } from 'react';
import { Api } from '../api/client.js';

export function SnapshotTrigger() {
  const [country, setCountry] = useState('BEN');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setStatus(null);
    try {
      const response = await Api.enqueueSnapshot({ country_iso3: country || undefined });
      setStatus(`Tâche planifiée (id: ${response.task_id})`);
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="snapshot-form" onSubmit={handleSubmit}>
      <label>
        ISO3 ciblé
        <input value={country} onChange={(e) => setCountry(e.target.value.toUpperCase())} maxLength={3} />
      </label>
      <button type="submit" disabled={loading}>
        {loading ? 'Envoi...' : 'Générer un snapshot'}
      </button>
      {status && <p className="status">{status}</p>}
    </form>
  );
}
