# Opérations & déploiement

## Secrets et rotation de tokens

- Les secrets doivent vivre dans `.env` ou dans un gestionnaire externe (Vault, AWS Secrets Manager...).
- Pour régénérer un token API sans supprimer le compte d’un utilisateur :
  ```bash
  ./venv/bin/python manage.py drf_create_token --regen <username>
  ```
- Après rotation, mettez à jour la variable `AUTH_TOKEN_NAME` pour tracer la date ou l’usage du nouveau token si besoin.
- `DJANGO_SECRET_KEY` et les clés de base de données doivent être renouvelées dès qu’un incident est suspecté. Redéployez ensuite les conteneurs ou services.

## Configuration CORS / hôtes

- `DJANGO_ALLOWED_HOSTS` contrôle les domaines autorisés côté Django.
- `CORS_ALLOWED_ORIGINS` et `CSRF_TRUSTED_ORIGINS` acceptent une liste séparée par des virgules (par ex. `https://app.ecopoweratlas.org`).
- Pour un accès local multiplateforme, laissez `CORS_ALLOW_ALL_ORIGINS=1`. En production, fixez-le à `0` et fournissez explicitement les origines approuvées.

## Journalisation et throttling

- Ajustez `DJANGO_LOG_LEVEL` (`INFO`, `WARNING`, `DEBUG`...) pour contrôler le niveau global.
- Les limites DRF se règlent avec `RATE_LIMIT_USER` et `RATE_LIMIT_ANON`. Format accepté : `nombre/intervalle` (ex. `5000/day`, `200/min`).
- Les logs sont émis sur stdout avec le format `[LEVEL] timestamp logger: message`. Redirigez-les vers votre stack observabilité en production.

## Docker & docker-compose

1. Construire l’image :
   ```bash
   docker compose build
   ```
2. Lancer la stack locale (PostgreSQL + API) :
   ```bash
   docker compose up
   ```
3. Les migrations + `collectstatic` tournent automatiquement avant `gunicorn`.
4. Pour rentrer dans le conteneur :
   ```bash
   docker compose exec web /bin/sh
   ```
5. La base PostgreSQL exposée via le service `db` (port 5432) avec les identifiants définis dans `docker-compose.yml`.

## Workers Celery

- Le service `worker` partage la même image que `web` et se connecte à Redis (`redis://redis:6379/0`).
- Pour lancer uniquement le worker :
  ```bash
  docker compose up worker
  ```
- Les tâches utilisent les paramètres `CELERY_TASK_ALWAYS_EAGER`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`.
- En local, laissez `CELERY_TASK_ALWAYS_EAGER=1` pour que les tâches s’exécutent immédiatement sans broker.

## Vérifications de sécurité

- Activez `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` et configurez `SECURE_HSTS_SECONDS` (>0) en production derrière TLS.
- Si vous êtes derrière un proxy (Nginx, Traefik), vérifiez que l’en-tête `X-Forwarded-Proto` est propagé afin que Django détecte correctement HTTPS.
