# Authentification API

Pour accéder aux endpoints en écriture :

1. Créer un utilisateur staff dans l’admin Django (`/admin/`) ou via :

```bash
./venv/bin/python manage.py createsuperuser --email admin@example.com --username admin
```

2. Générer un token :

```bash
./venv/bin/python manage.py drf_create_token admin
```

3. Stocker la clé obtenue (ex. `f5977761dc5a6f2b39e0713b0d4a341eaa3cfd7a`) dans un coffre, puis la diffuser aux systèmes concernés.

4. Utiliser ce token :

```
Authorization: Token <clé>
```

Les opérations en lecture restent publiques (`IsAuthenticatedOrReadOnly`).

## Rotation de token

Pour régénérer un token déjà existant (incident de sécurité, employé qui quitte l’équipe, etc.) :

```bash
./venv/bin/python manage.py drf_create_token --regen <username>
```

Le nouveau token remplace l’ancien immédiatement. Pensez à invalider l’ancien secret dans vos stores et à mettre à jour la variable `AUTH_TOKEN_NAME` si vous suivez les versions de clé.
