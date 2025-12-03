# Import de données

## Ressources (CSV/XLSX)

Commande :

```bash
./venv/bin/python manage.py import_resources data/samples/resource_metrics_sample.csv \
  --dataset-name "Potential 2024" \
  --resource-type solar \
  --default-metric solar_potential_kwh_m2
```

Colonnes attendues :
- `iso3` (obligatoire)
- `country` (optionnel)
- `metric` (sinon `--default-metric`)
- `value` (obligatoire)
- `unit`, `year` (optionnels)

## GeoJSON

```bash
./venv/bin/python manage.py import_geojson data/samples/countries_sample.geojson --target country
```

Pour des régions :

```bash
./venv/bin/python manage.py import_geojson data/samples/benin_regions.geojson \
  --target region --country-iso3 BEN --name-field district
```

Champs utilisés par défaut : `iso3`, `name`, `geometry`. Utiliser les options `--name-field`, `--iso3-field`, `--level` selon vos fichiers.
