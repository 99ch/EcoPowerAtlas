import csv
from io import StringIO

from django.db.models import Count, Sum
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers
from .permissions import IsStaffOrReadOnly



@extend_schema_view(
	list=extend_schema(tags=['Countries']),
	retrieve=extend_schema(tags=['Countries']),
	create=extend_schema(tags=['Countries']),
	update=extend_schema(tags=['Countries']),
	partial_update=extend_schema(tags=['Countries']),
	destroy=extend_schema(tags=['Countries']),
)
class CountryViewSet(viewsets.ModelViewSet):
	queryset = models.Country.objects.all().annotate(
		region_count=Count('regions'),
		site_count=Count('hydro_sites'),
	).order_by('name')
	serializer_class = serializers.CountrySerializer
	permission_classes = [IsStaffOrReadOnly]
	filterset_fields = ['iso2', 'iso3']
	search_fields = ['name']
	ordering_fields = ['name', 'population', 'created_at']


@extend_schema_view(
	list=extend_schema(tags=['Regions']),
	retrieve=extend_schema(tags=['Regions']),
	create=extend_schema(tags=['Regions']),
	update=extend_schema(tags=['Regions']),
	partial_update=extend_schema(tags=['Regions']),
	destroy=extend_schema(tags=['Regions']),
)
class RegionViewSet(viewsets.ModelViewSet):
	queryset = models.Region.objects.select_related('country').all().order_by('country__name', 'name')
	serializer_class = serializers.RegionSerializer
	permission_classes = [IsStaffOrReadOnly]
	filterset_fields = ['country__iso3', 'level']
	search_fields = ['name']
	ordering_fields = ['name', 'country__name']


@extend_schema_view(
	list=extend_schema(tags=['Datasets']),
	retrieve=extend_schema(tags=['Datasets']),
	create=extend_schema(tags=['Datasets']),
	update=extend_schema(tags=['Datasets']),
	partial_update=extend_schema(tags=['Datasets']),
	destroy=extend_schema(tags=['Datasets']),
)
class EnergyDatasetViewSet(viewsets.ModelViewSet):
	queryset = models.EnergyDataset.objects.all().order_by('name')
	serializer_class = serializers.EnergyDatasetSerializer
	permission_classes = [IsStaffOrReadOnly]
	filterset_fields = ['dataset_type']
	search_fields = ['name', 'source']
	ordering_fields = ['name', 'created_at']


@extend_schema_view(
	list=extend_schema(tags=['Hydro Sites']),
	retrieve=extend_schema(tags=['Hydro Sites']),
	create=extend_schema(tags=['Hydro Sites']),
	update=extend_schema(tags=['Hydro Sites']),
	partial_update=extend_schema(tags=['Hydro Sites']),
	destroy=extend_schema(tags=['Hydro Sites']),
)
class HydroSiteViewSet(viewsets.ModelViewSet):
	queryset = models.HydroSite.objects.select_related('country', 'region', 'dataset').all().order_by('name')
	serializer_class = serializers.HydroSiteSerializer
	permission_classes = [IsStaffOrReadOnly]
	filterset_fields = [
		'country__iso3',
		'region__name',
		'status',
		'dataset',
	]
	search_fields = ['name', 'notes', 'properties']
	ordering_fields = ['name', 'head_m', 'storage_capacity_mwh', 'turbine_capacity_mw']

	@extend_schema(
		tags=['Hydro Sites'],
		summary='Résumé global',
		description='Retourne des agrégats sur les sites filtrés (totaux stockage/capacité, top pays).',
	)
	@action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
	def summary(self, request):
		queryset = self.filter_queryset(self.get_queryset())
		aggregates = queryset.aggregate(
			total_sites=Count('id'),
			total_storage=Sum('storage_capacity_mwh'),
			total_capacity=Sum('turbine_capacity_mw'),
		)
		top_countries = list(
			queryset.values('country__iso3', 'country__name')
			.annotate(site_count=Count('id'))
			.order_by('-site_count')[:5]
		)
		return Response({
			'total_sites': aggregates['total_sites'] or 0,
			'total_storage_mwh': float(aggregates['total_storage'] or 0),
			'total_capacity_mw': float(aggregates['total_capacity'] or 0),
			'top_countries': top_countries,
		})

	@extend_schema(
		tags=['Hydro Sites'],
		summary='Export CSV',
		description='Exporte les sites filtrés au format CSV.',
		parameters=[
			OpenApiParameter('country__iso3', str, OpenApiParameter.QUERY, description='Filtre par pays'),
		],
	)
	@action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
	def export(self, request):
		queryset = self.filter_queryset(self.get_queryset())
		buffer = StringIO()
		writer = csv.writer(buffer)
		writer.writerow([
			'id',
			'name',
			'country_iso3',
			'region',
			'latitude',
			'longitude',
			'head_m',
			'storage_capacity_mwh',
			'turbine_capacity_mw',
			'status',
		])
		for site in queryset:
			writer.writerow([
				site.id,
				site.name,
				site.country.iso3,
				site.region.name if site.region else '',
				site.latitude,
				site.longitude,
				site.head_m,
				site.storage_capacity_mwh,
				site.turbine_capacity_mw,
				site.status,
			])
		buffer.seek(0)
		response = Response(buffer.getvalue(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="hydro_sites.csv"'
		return response


@extend_schema_view(
	list=extend_schema(tags=['Resource Metrics']),
	retrieve=extend_schema(tags=['Resource Metrics']),
	create=extend_schema(tags=['Resource Metrics']),
	update=extend_schema(tags=['Resource Metrics']),
	partial_update=extend_schema(tags=['Resource Metrics']),
	destroy=extend_schema(tags=['Resource Metrics']),
)
class ResourceMetricViewSet(viewsets.ModelViewSet):
	queryset = models.ResourceMetric.objects.select_related('country', 'region', 'dataset').all().order_by('-created_at')
	serializer_class = serializers.ResourceMetricSerializer
	permission_classes = [IsStaffOrReadOnly]
	filterset_fields = ['resource_type', 'country__iso3', 'year']
	search_fields = ['metric']
	ordering_fields = ['value', 'year']

	@extend_schema(
		tags=['Resource Metrics'],
		summary='Export CSV',
		description='Exporte les métriques filtrées en CSV.',
	)
	@action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
	def export(self, request):
		queryset = self.filter_queryset(self.get_queryset())
		buffer = StringIO()
		writer = csv.writer(buffer)
		writer.writerow(['country_iso3', 'resource_type', 'metric', 'value', 'unit', 'year'])
		for metric in queryset:
			writer.writerow([
				metric.country.iso3,
				metric.resource_type,
				metric.metric,
				metric.value,
				metric.unit,
				metric.year,
			])
		buffer.seek(0)
		response = Response(buffer.getvalue(), content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="resource_metrics.csv"'
		return response


@extend_schema_view(
	list=extend_schema(tags=['Climate Series']),
	retrieve=extend_schema(tags=['Climate Series']),
	create=extend_schema(tags=['Climate Series']),
	update=extend_schema(tags=['Climate Series']),
	partial_update=extend_schema(tags=['Climate Series']),
	destroy=extend_schema(tags=['Climate Series']),
)
class ClimateSeriesViewSet(viewsets.ModelViewSet):
	queryset = models.ClimateSeries.objects.select_related('country', 'region', 'site', 'dataset').all().order_by('-created_at')
	serializer_class = serializers.ClimateSeriesSerializer
	permission_classes = [IsStaffOrReadOnly]
	filterset_fields = ['variable', 'country__iso3', 'site']
	search_fields = ['variable']
	ordering_fields = ['created_at']


@extend_schema(tags=['Stats'])
class StatsViewSet(viewsets.ViewSet):
	permission_classes = [permissions.AllowAny]

	def list(self, request):
		country_stats = models.Country.objects.annotate(site_count=Count('hydro_sites')).order_by('-site_count')[:5]
		resource_stats = models.ResourceMetric.objects.values('resource_type').annotate(
			total=Sum('value'),
			metrics=Count('id'),
		).order_by('resource_type')
		return Response({
			'countries': [
				{'iso3': country.iso3, 'name': country.name, 'site_count': country.site_count}
				for country in country_stats
			],
			'resources': list(resource_stats),
			'dataset_count': models.EnergyDataset.objects.count(),
		})

	@extend_schema(
		tags=['Stats'],
		parameters=[OpenApiParameter('iso3', str, OpenApiParameter.QUERY, description='Code ISO3 du pays')],
	)
	@action(detail=False, methods=['get'])
	def by_country(self, request):
		iso3 = request.query_params.get('iso3')
		if not iso3:
			return Response({'detail': 'Paramètre iso3 requis.'}, status=status.HTTP_400_BAD_REQUEST)
		country = models.Country.objects.filter(iso3__iexact=iso3).first()
		if not country:
			return Response({'detail': 'Pays introuvable.'}, status=status.HTTP_404_NOT_FOUND)
		resource_summary = models.ResourceMetric.objects.filter(country=country).values('resource_type').annotate(
			total=Sum('value'),
			metrics=Count('id'),
		)
		site_summary = models.HydroSite.objects.filter(country=country).aggregate(
			total_sites=Count('id'),
			total_storage=Sum('storage_capacity_mwh'),
			total_capacity=Sum('turbine_capacity_mw'),
		)
		return Response({
			'country': country.name,
			'site_summary': {
				'total_sites': site_summary['total_sites'] or 0,
				'total_storage_mwh': float(site_summary['total_storage'] or 0),
				'total_capacity_mw': float(site_summary['total_capacity'] or 0),
			},
			'resource_summary': list(resource_summary),
		})
