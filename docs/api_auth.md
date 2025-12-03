# Authentification API

Pour accéder aux endpoints en écriture :

1. Créer un utilisateur staff dans l’admin Django (`/admin/`).
2. Générer un token :

```bash
/Volumes/linux/bureau/EcoPowerAtlas/venv/bin/python manage.py drf_create_token <email>
```

3. Utiliser ce token dans les requêtes :

```
Authorization: Token <clé>
```

Les opérations en lecture restent publiques (permissions `IsAuthenticatedOrReadOnly`).
