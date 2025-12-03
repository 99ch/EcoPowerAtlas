import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from core import models


class Command(BaseCommand):
    help = "Charge des géométries GeoJSON dans les pays ou régions."

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Fichier GeoJSON (.geojson).')
        parser.add_argument('--target', choices=['country', 'region'], default='country')
        parser.add_argument('--country-iso3', dest='country_iso3', help='ISO3 cible (pour les régions).')
        parser.add_argument('--name-field', dest='name_field', default='name')
        parser.add_argument('--iso3-field', dest='iso3_field', default='iso3')
        parser.add_argument('--level', default='')

    def handle(self, *args, **options):
        path = Path(options['path']).expanduser()
        if not path.exists():
            raise CommandError(f'Fichier introuvable: {path}')
        data = json.loads(path.read_text(encoding='utf-8'))
        features = data.get('features', [])
        if not features:
            raise CommandError('Aucune entité trouvée dans le GeoJSON.')

        if options['target'] == 'country':
            imported = self._import_countries(features, options)
        else:
            imported = self._import_regions(features, options)
        self.stdout.write(self.style.SUCCESS(f'{imported} géométries importées.'))

    def _import_countries(self, features, options):
        imported = 0
        for feature in features:
            props = feature.get('properties', {})
            iso3 = (props.get(options['iso3_field']) or props.get('iso_a3') or props.get('ISO_A3') or '').strip().upper()
            if not iso3:
                continue
            name = props.get(options['name_field']) or props.get('name') or props.get('NAME') or iso3
            iso2 = props.get('iso_a2') or props.get('ISO_A2') or iso3[:2]
            boundary = feature.get('geometry')
            models.Country.objects.update_or_create(
                iso3=iso3,
                defaults={'name': name, 'iso2': iso2, 'boundary': boundary},
            )
            imported += 1
        return imported

    def _import_regions(self, features, options):
        imported = 0
        for feature in features:
            props = feature.get('properties', {})
            country_iso3 = (props.get('country_iso3') or options['country_iso3'] or '').strip().upper()
            if not country_iso3:
                continue
            country = models.Country.objects.filter(iso3=country_iso3).first()
            if not country:
                self.stdout.write(self.style.WARNING(f'Pays {country_iso3} introuvable, région ignorée.'))
                continue
            name = props.get(options['name_field']) or props.get('name') or props.get('NAME')
            if not name:
                continue
            boundary = feature.get('geometry')
            models.Region.objects.update_or_create(
                country=country,
                name=name,
                defaults={'boundary': boundary, 'level': options['level'] or props.get('level', '')},
            )
            imported += 1
        return imported
