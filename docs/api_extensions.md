# Extensions API

## Pagination personnalisée

- Paramètre `page_size` disponible sur tous les endpoints paginés.
- Taille par défaut (`API_DEFAULT_PAGE_SIZE`) et maximum (`API_MAX_PAGE_SIZE`) configurables via `.env`.
- Exemple : `/api/countries/?page=2&page_size=20`.

## Séries temporelles des métriques

- Endpoint : `GET /api/resource-metrics/timeseries/`.
- Paramètres : `country__iso3`, `resource_type`.
- Réponse : tableau d’objets `{"year": 2024, "total_value": 1234.5, "data_points": 3}`.

## Timeline climat

- Endpoint : `GET /api/climate-series/timeline/?variable=rainfall&country__iso3=BEN`.
- Paramètres facultatifs : `site`, `limit` (par défaut 500, max 2000).
- Retourne jusqu’à 5 séries correspondantes avec les points tronqués selon `limit`.

## Tâches asynchrones

- Endpoint : `POST /api/resource-metrics/enqueue_snapshot/`.
- Payload : `{ "country_iso3": "BEN" }` (optionnel).
- Réponse : `{"task_id": "uuid"}`.
- Le worker Celery générera un agrégat (`core.tasks.generate_metric_snapshot`) et journalisera l’évènement.
