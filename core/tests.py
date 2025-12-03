from django.test import TestCase
from rest_framework.test import APIClient

from . import models


class CountryModelTest(TestCase):
	def test_str_returns_name(self):
		benin = models.Country.objects.create(name='Benin', iso2='BJ', iso3='BEN')
		self.assertEqual(str(benin), 'Benin')


class CountryAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.dataset = models.EnergyDataset.objects.create(
			name='Test Dataset',
			dataset_type='phes',
		)
		self.country = models.Country.objects.create(name='Benin', iso2='BJ', iso3='BEN')
		self.region = models.Region.objects.create(country=self.country, name='Atlantique')
		models.HydroSite.objects.create(
			name='Site A',
			country=self.country,
			region=self.region,
			dataset=self.dataset,
		)

	def test_list_countries_returns_data(self):
		response = self.client.get('/api/countries/')
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertGreaterEqual(payload['count'], 1)
		self.assertEqual(payload['results'][0]['iso3'], 'BEN')

	def test_filter_hydro_sites_by_country(self):
		response = self.client.get('/api/hydro-sites/', {'country__iso3': 'BEN'})
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload['count'], 1)

