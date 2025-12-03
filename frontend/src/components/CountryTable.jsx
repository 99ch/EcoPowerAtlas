import { useEffect, useState } from 'react';
import { Api } from '../api/client.js';
import { Loader } from './Loader.jsx';

const PAGE_SIZE_OPTIONS = [10, 20, 50];

export function CountryTable() {
  const [data, setData] = useState({ results: [], count: 0 });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    Api.getCountries({ page, page_size: pageSize, search })
      .then((response) => {
        if (!cancelled) setData(response);
      })
      .catch((err) => !cancelled && setError(err.message))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [page, pageSize, search]);

  const totalPages = Math.max(1, Math.ceil(data.count / pageSize));

  if (loading) return <Loader label="Chargement des pays" />;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="country-table">
      <div className="table-controls">
        <input
          type="search"
          placeholder="Rechercher un pays"
          value={search}
          onChange={(e) => {
            setPage(1);
            setSearch(e.target.value);
          }}
        />
        <select value={pageSize} onChange={(e) => setPageSize(Number(e.target.value))}>
          {PAGE_SIZE_OPTIONS.map((size) => (
            <option key={size} value={size}>
              {size} / page
            </option>
          ))}
        </select>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>ISO3</th>
              <th>Population</th>
              <th>Sites</th>
            </tr>
          </thead>
          <tbody>
            {data.results.map((country) => (
              <tr key={country.id}>
                <td>{country.name}</td>
                <td>{country.iso3}</td>
                <td>{country.population?.toLocaleString('fr-FR') ?? '—'}</td>
                <td>{country.site_count ?? 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="pagination">
        <button onClick={() => setPage((prev) => Math.max(1, prev - 1))} disabled={page === 1}>
          Précédent
        </button>
        <span>
          Page {page} / {totalPages}
        </span>
        <button onClick={() => setPage((prev) => Math.min(totalPages, prev + 1))} disabled={page === totalPages}>
          Suivant
        </button>
      </div>
    </div>
  );
}
