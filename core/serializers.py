from rest_framework import serializers

from . import models


class CountrySerializer(serializers.ModelSerializer):
    region_count = serializers.IntegerField(read_only=True, default=0)
    site_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = models.Country
        fields = [
            'id',
            'name',
            'iso2',
            'iso3',
            'population',
            'boundary',
            'region_count',
            'site_count',
            'created_at',
            'updated_at',
        ]


class RegionSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = models.Region
        fields = [
            'id',
            'country',
            'country_name',
            'name',
            'level',
            'boundary',
            'created_at',
            'updated_at',
        ]


class EnergyDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnergyDataset
        fields = '__all__'


class HydroSiteSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = models.HydroSite
        fields = [
            'id',
            'name',
            'country',
            'country_name',
            'region',
            'region_name',
            'dataset',
            'latitude',
            'longitude',
            'elevation_m',
            'head_m',
            'storage_capacity_mwh',
            'turbine_capacity_mw',
            'status',
            'notes',
            'properties',
            'created_at',
            'updated_at',
        ]


class ResourceMetricSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = models.ResourceMetric
        fields = [
            'id',
            'dataset',
            'country',
            'country_name',
            'region',
            'region_name',
            'resource_type',
            'metric',
            'value',
            'unit',
            'year',
            'created_at',
            'updated_at',
        ]


class ClimateSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClimateSeries
        fields = '__all__'
