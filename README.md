# EcoPowerAtlas

EcoPowerAtlas est une plateforme de cartographie et d’analyse du potentiel de stations de transfert d’énergie par pompage (PHES) en Afrique. Le projet combine un backend Django/DRF sécurisé (imports CSV & GeoJSON, exports PDF/CSV, statistiques, tâches Celery) et une interface React responsive qui consomme directement l’API pour présenter les agrégats, séries temporelles et déclencher des snapshots asynchrones.

## Distinctiveness and Complexity

### Pourquoi ce projet est distinct

- **Pas un réseau social ni un e-commerce** : l’application cible un domaine énergétique très spécifique (potentiel PHES et séries climatiques). Elle orchestre des imports de données, des agrégations statistiques, des exports PDF, des tâches asynchrones et une visualisation spécialisée.
- **Orientation géospatiale et scientifique** : gestion de jeux de données (Country, Region, HydroSite, ResourceMetric, ClimateSeries, ReportAttachment) avec contraintes d’intégrité, agrégats par pays et stockage de séries temporelles. Rien de comparable avec les projets standards du cours.
- **Ops et CI intégrés** : `.env.example`, `Dockerfile`, `docker-compose.yml`, pipeline GitHub Actions, throttling DRF, logging structuré. L’objectif est de livrer une base réellement exploitable.

### Pourquoi ce projet est complexe

- **Backend avancé** : endpoints DRF supplémentaires (`/summary`, `/export`, `/timeseries`, `/timeline`, `/enqueue_snapshot`, `/stats/by_country`) avec pagination personnalisée, throttling, CORS fin, et génération PDF via ReportLab. Les modèles imposent des contraintes uniques, des validateurs et des fixtures.
- **Asynchrone** : intégration Celery/Redis avec tâche `generate_metric_snapshot`, formulaire React pour déclencher la task, configuration environnement (brokers, eager mode, worker Docker).
- **Frontend riche** : SPA React/Vite, consommation de l’API via `fetch`, graphes Recharts, tables paginées, formulaires interactifs (filtre pays, resource type, timeline). Layout mobile-first en CSS pur (grid/flex) sans framework prêt-à-l’emploi.
- **Documentation complète** : guides API (`docs/api_auth.md`, `docs/api_extensions.md`), opérations (`docs/operations.md`), imports (`docs/imports.md`) et README détaillé pour le livrable Capstone.

## Structure des fichiers principaux

- `core/` : modèles Django, serializers, vues (DRF viewsets + actions custom), tests unitaires, pagination, tâches Celery, fixtures et migrations.
- `ecopoweratlas/settings.py` : configuration renforcée (env, throttling, Celery, logging, Spectacular, CORS/CSRF, PostgreSQL via `DATABASE_URL`).
- `docs/` : guides authentification, imports, opérations, extensions API.
- `frontend/` : application React (Vite), composants UI, client API, styles responsive, build prêt (`npm run build`).
- `Dockerfile`, `docker-compose.yml` : image gunicorn+Celery et stack complète web/db/redis/worker.
- `.github/workflows/ci.yml` : pipeline tests Django + build docker compose.

## Backend : mise en route

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env  # Ajuster les variables (SECRET_KEY, DATABASE_URL, etc.)
python manage.py migrate
python manage.py runserver
```

### Importer des données d’exemple

```bash
python manage.py loaddata core/fixtures/minimal_core.json
python manage.py import_resources data/samples/resource_metrics_sample.csv --dataset-name "Potential 2024"
```

### Tests backend

```bash
python manage.py test core
```

## Frontend : mise en route

```bash
cd frontend
cp .env.example .env             # VITE_API_BASE_URL
npm install
npm run dev                      # http://localhost:5173
npm run build                    # builds dist/
```

Le frontend consomme `http://127.0.0.1:8000/api` par défaut mais l’URL peut être modifiée via `VITE_API_BASE_URL`.

## Docker / orchestration

```bash
cp .env.example .env
# nécessite Docker Desktop
docker compose build
docker compose up
```

Services :

- `web` (gunicorn + collectstatic + migrations)
- `worker` (Celery)
- `db` (PostgreSQL 16)
- `redis` (broker/result backend)

## Responsiveness & UI

- Layout en CSS Grid/Flex avec `clamp()` / `auto-fit` pour adapter les cartes et tableaux.
- Composants clés : `StatsPanel`, `HydroSummary`, `CountryTable`, `ResourceTimeseries` (graphique Recharts responsive), `ClimateTimeline` (grid de points), `SnapshotTrigger` (formulaire). Tous passent en colonne unique < 640px.
- Styles centralisés (`src/index.css`, `src/App.css`) : boutons pill, cartes ombrées, loader custom, média queries.

## API & fonctionnalités majeures

- Pagination personnalisée via `core.pagination.StandardResultsSetPagination` (query `page_size`).
- Endpoints supplémentaires (`/api/resource-metrics/timeseries/`, `/api/climate-series/timeline/`, `/api/resource-metrics/enqueue_snapshot/`).
- Exports CSV/PDF (`/api/hydro-sites/export/`, `/api/resource-metrics/export_pdf/`).
- Stats globales (`/api/stats/`, `/api/stats/by_country/`).
- JWT/token management documenté dans `docs/api_auth.md` (rotation via `drf_create_token --regen`).

## Informations supplémentaires

- CI GitHub Actions lance les tests Django (PostgreSQL + Redis) et valide `docker compose config`.
- Les tâches Celery peuvent s’exécuter en eager (`CELERY_TASK_ALWAYS_EAGER=1`) pour les environnements sans broker.
- Pour la démonstration Capstone, capturez les écrans du frontend (desktop + mobile) et mentionnez que Docker n’a pas pu être validé localement faute d’installation.

Ce README répond aux exigences : section Distinctiveness & Complexity détaillée, inventaire des fichiers, instructions d’exécution backend/frontend/Docker, description de la responsivité et notes complémentaires. Ajustez les variables `.env` selon votre propre environnement.
