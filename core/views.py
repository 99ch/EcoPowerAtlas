from django.db.models import Count
from rest_framework import viewsets

from . import models, serializers


class CountryViewSet(viewsets.ModelViewSet):
	queryset = models.Country.objects.all().annotate(
		region_count=Count('regions'),
		site_count=Count('hydro_sites'),
	).order_by('name')
	serializer_class = serializers.CountrySerializer
	filterset_fields = ['iso2', 'iso3']
	search_fields = ['name']
	ordering_fields = ['name', 'population', 'created_at']


class RegionViewSet(viewsets.ModelViewSet):
	queryset = models.Region.objects.select_related('country').all().order_by('country__name', 'name')
	serializer_class = serializers.RegionSerializer
	filterset_fields = ['country__iso3', 'level']
	search_fields = ['name']
	ordering_fields = ['name', 'country__name']


class EnergyDatasetViewSet(viewsets.ModelViewSet):
	queryset = models.EnergyDataset.objects.all().order_by('name')
	serializer_class = serializers.EnergyDatasetSerializer
	filterset_fields = ['dataset_type']
	search_fields = ['name', 'source']
	ordering_fields = ['name', 'created_at']


class HydroSiteViewSet(viewsets.ModelViewSet):
	queryset = models.HydroSite.objects.select_related('country', 'region', 'dataset').all().order_by('name')
	serializer_class = serializers.HydroSiteSerializer
	filterset_fields = [
		'country__iso3',
		'region__name',
		'status',
		'dataset',
	]
	search_fields = ['name', 'notes', 'properties']
	ordering_fields = ['name', 'head_m', 'storage_capacity_mwh', 'turbine_capacity_mw']


class ResourceMetricViewSet(viewsets.ModelViewSet):
	queryset = models.ResourceMetric.objects.select_related('country', 'region', 'dataset').all().order_by('-created_at')
	serializer_class = serializers.ResourceMetricSerializer
	filterset_fields = ['resource_type', 'country__iso3', 'year']
	search_fields = ['metric']
	ordering_fields = ['value', 'year']


class ClimateSeriesViewSet(viewsets.ModelViewSet):
	queryset = models.ClimateSeries.objects.select_related('country', 'region', 'site', 'dataset').all().order_by('-created_at')
	serializer_class = serializers.ClimateSeriesSerializer
	filterset_fields = ['variable', 'country__iso3', 'site']
	search_fields = ['variable']
	ordering_fields = ['created_at']
