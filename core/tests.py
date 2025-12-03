from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from . import models


class CountryModelTest(TestCase):
	def test_str_returns_name(self):
		benin = models.Country.objects.create(name='Benin', iso2='BJ', iso3='BEN')
		self.assertEqual(str(benin), 'Benin')


class APITestBase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.dataset = models.EnergyDataset.objects.create(
			name='Test Dataset',
			dataset_type='phes',
		)
		self.country = models.Country.objects.create(name='Benin', iso2='BJ', iso3='BEN')
		self.region = models.Region.objects.create(country=self.country, name='Atlantique')
		self.site = models.HydroSite.objects.create(
			name='Site A',
			country=self.country,
			region=self.region,
			dataset=self.dataset,
			head_m=100,
			storage_capacity_mwh=50,
		)
		models.ResourceMetric.objects.create(
			dataset=models.EnergyDataset.objects.create(name='Resources', dataset_type='resource'),
			country=self.country,
			resource_type='solar',
			metric='potential',
			value=123.4,
			unit='kWh/m2',
		)


class CountryAPITest(APITestBase):
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

	def test_stats_endpoint_returns_totals(self):
		response = self.client.get('/api/stats/')
		self.assertEqual(response.status_code, 200)
		self.assertIn('dataset_count', response.json())

	def test_hydro_site_summary_action(self):
		response = self.client.get('/api/hydro-sites/summary/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['total_sites'], 1)

	def test_hydro_site_export_action(self):
		response = self.client.get('/api/hydro-sites/export/')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response['Content-Disposition'].startswith('attachment;'))

	def test_resource_metric_export_action(self):
		response = self.client.get('/api/resource-metrics/export/')
		self.assertEqual(response.status_code, 200)
		self.assertIn('resource_type', response.content.decode())

	def test_resource_metric_pdf(self):
		response = self.client.get('/api/resource-metrics/export_pdf/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'application/pdf')

	def test_stats_by_country_requires_iso3(self):
		response = self.client.get('/api/stats/by_country/')
		self.assertEqual(response.status_code, 400)

	def test_stats_by_country_returns_data(self):
		response = self.client.get('/api/stats/by_country/', {'iso3': 'BEN'})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['country'], 'Benin')


class PermissionTest(APITestBase):
	def setUp(self):
		super().setUp()
		self.user = get_user_model().objects.create_user('user@example.com', 'user@example.com', 'password')
		self.staff = get_user_model().objects.create_user('staff@example.com', 'staff@example.com', 'password', is_staff=True)

	def test_non_staff_cannot_create_hydro_site(self):
		payload = {
			'name': 'Site B',
			'country': self.country.id,
			'head_m': 50,
		}
		client = APIClient()
		client.force_authenticate(self.user)
		response = client.post('/api/hydro-sites/', payload, format='json')
		self.assertEqual(response.status_code, 403)

	def test_staff_can_create_hydro_site(self):
		payload = {
			'name': 'Site Staff',
			'country': self.country.id,
			'head_m': 40,
		}
		client = APIClient()
		client.force_authenticate(self.staff)
		response = client.post('/api/hydro-sites/', payload, format='json')
		self.assertEqual(response.status_code, 201)

