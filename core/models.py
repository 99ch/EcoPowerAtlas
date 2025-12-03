from django.db import models


class TimeStampedModel(models.Model):
	"""Abstract base model with audit fields."""

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Country(TimeStampedModel):
	name = models.CharField(max_length=128, unique=True)
	iso2 = models.CharField(max_length=2, unique=True)
	iso3 = models.CharField(max_length=3, unique=True)
	population = models.BigIntegerField(null=True, blank=True)
	boundary = models.JSONField(null=True, blank=True, help_text="GeoJSON geometry")

	class Meta:
		ordering = ['name']

	def __str__(self) -> str:  # pragma: no cover - trivial
		return self.name


class Region(TimeStampedModel):
	country = models.ForeignKey(Country, related_name='regions', on_delete=models.CASCADE)
	name = models.CharField(max_length=128)
	level = models.CharField(max_length=64, blank=True)
	boundary = models.JSONField(null=True, blank=True)

	class Meta:
		unique_together = ('country', 'name')
		ordering = ['country__name', 'name']

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"{self.name} ({self.country.iso3})"


class EnergyDataset(TimeStampedModel):
	"""Represents an imported dataset containing energy metrics."""

	DATASET_TYPES = [
		('resource', 'Resource Potential'),
		('climate', 'Climate'),
		('phes', 'PHES Sites'),
	]

	name = models.CharField(max_length=128)
	dataset_type = models.CharField(max_length=24, choices=DATASET_TYPES)
	source = models.CharField(max_length=256, blank=True)
	description = models.TextField(blank=True)
	file_name = models.CharField(max_length=256, blank=True)
	file_checksum = models.CharField(max_length=128, blank=True)
	metadata = models.JSONField(default=dict, blank=True)

	class Meta:
		ordering = ['name']

	def __str__(self) -> str:  # pragma: no cover - trivial
		return self.name


class HydroSite(TimeStampedModel):
	STATUS_CHOICES = [
		('identified', 'Identified'),
		('study', 'Feasibility Study'),
		('construction', 'Under Construction'),
		('operational', 'Operational'),
	]

	country = models.ForeignKey(Country, related_name='hydro_sites', on_delete=models.PROTECT)
	region = models.ForeignKey(Region, related_name='hydro_sites', on_delete=models.SET_NULL, null=True, blank=True)
	dataset = models.ForeignKey(EnergyDataset, related_name='hydro_sites', on_delete=models.SET_NULL, null=True, blank=True)
	name = models.CharField(max_length=128)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	elevation_m = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	head_m = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
	storage_capacity_mwh = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	turbine_capacity_mw = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
	status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='identified')
	notes = models.TextField(blank=True)
	properties = models.JSONField(default=dict, blank=True)

	class Meta:
		ordering = ['country__name', 'name']

	def __str__(self) -> str:  # pragma: no cover - trivial
		return self.name


class ResourceMetric(TimeStampedModel):
	RESOURCE_TYPES = [
		('solar', 'Solar'),
		('wind', 'Wind'),
		('hydro', 'Hydro'),
		('biomass', 'Biomass'),
		('other', 'Other'),
	]

	dataset = models.ForeignKey(EnergyDataset, related_name='metrics', on_delete=models.CASCADE)
	country = models.ForeignKey(Country, related_name='resource_metrics', on_delete=models.CASCADE)
	region = models.ForeignKey(Region, related_name='resource_metrics', on_delete=models.SET_NULL, null=True, blank=True)
	resource_type = models.CharField(max_length=16, choices=RESOURCE_TYPES)
	metric = models.CharField(max_length=64)
	value = models.DecimalField(max_digits=14, decimal_places=4)
	unit = models.CharField(max_length=32, default='')
	year = models.PositiveIntegerField(null=True, blank=True)

	class Meta:
		ordering = ['resource_type', 'country__name', 'metric']

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"{self.resource_type} {self.metric} ({self.country.iso3})"


class ClimateSeries(TimeStampedModel):
	dataset = models.ForeignKey(EnergyDataset, related_name='climate_series', on_delete=models.CASCADE)
	country = models.ForeignKey(Country, related_name='climate_series', on_delete=models.CASCADE)
	region = models.ForeignKey(Region, related_name='climate_series', on_delete=models.SET_NULL, null=True, blank=True)
	site = models.ForeignKey(HydroSite, related_name='climate_series', on_delete=models.SET_NULL, null=True, blank=True)
	variable = models.CharField(max_length=64)
	unit = models.CharField(max_length=32)
	statistics = models.JSONField(default=dict, blank=True, help_text="Precomputed indicators (mean, p90, etc.)")
	series = models.JSONField(default=list, blank=True, help_text="Serialized time series data")

	class Meta:
		ordering = ['variable', 'country__name']

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"{self.variable} - {self.country.iso3}"

