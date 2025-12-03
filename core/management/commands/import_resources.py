import csv
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from core import models


class Command(BaseCommand):
    help = "Importe des métriques de ressources à partir d'un fichier CSV ou Excel."

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Chemin du fichier à importer (CSV ou XLSX).')
        parser.add_argument('--dataset-name', dest='dataset_name', default='Ressources importées')
        parser.add_argument('--dataset-source', dest='dataset_source', default='')
        parser.add_argument('--resource-type', dest='resource_type', default='solar')
        parser.add_argument('--default-metric', dest='default_metric', default='potential_kwh')

    def handle(self, *args, **options):
        path = Path(options['path']).expanduser()
        if not path.exists():
            raise CommandError(f'Fichier introuvable: {path}')

        dataset, _ = models.EnergyDataset.objects.get_or_create(
            name=options['dataset_name'],
            defaults={
                'dataset_type': 'resource',
                'source': options['dataset_source'],
            },
        )

        rows = self._load_rows(path)
        created = 0
        for row in rows:
            iso3 = (row.get('iso3') or row.get('ISO3') or '').strip().upper()
            if not iso3:
                self.stdout.write(self.style.WARNING('Ligne ignorée: iso3 manquant.'))
                continue
            country_name = (row.get('country') or row.get('Country') or iso3).strip()
            iso2 = (row.get('iso2') or row.get('ISO2') or iso3[:2]).strip().upper()
            country, _ = models.Country.objects.get_or_create(
                iso3=iso3,
                defaults={'name': country_name, 'iso2': iso2},
            )

            metric_name = row.get('metric') or row.get('Metric') or options['default_metric']
            unit = row.get('unit') or row.get('Unit') or ''
            year = row.get('year') or row.get('Year')
            value = row.get('value') or row.get('Value')
            try:
                value = float(value)
            except (TypeError, ValueError):
                self.stdout.write(self.style.WARNING(f'Valeur invalide pour {iso3}/{metric_name}, ligne ignorée.'))
                continue

            models.ResourceMetric.objects.update_or_create(
                dataset=dataset,
                country=country,
                resource_type=options['resource_type'],
                metric=metric_name,
                defaults={'value': value, 'unit': unit, 'year': year},
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'{created} métriques importées vers {dataset.name}.'))

    def _load_rows(self, path: Path):
        suffix = path.suffix.lower()
        if suffix in {'.csv', '.txt'}:
            return self._read_csv(path)
        if suffix in {'.xlsx', '.xls'}:
            return self._read_excel(path)
        raise CommandError(f'Extension de fichier non supportée: {suffix}')

    def _read_csv(self, path: Path):
        with path.open('r', encoding='utf-8-sig') as fh:
            return list(csv.DictReader(fh))

    def _read_excel(self, path: Path):
        df = pd.read_excel(path)
        return df.to_dict(orient='records')
