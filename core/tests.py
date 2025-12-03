from django.test import TestCase

from . import models


class CountryModelTest(TestCase):
	def test_str_returns_name(self):
		benin = models.Country.objects.create(name='Benin', iso2='BJ', iso3='BEN')
		self.assertEqual(str(benin), 'Benin')

