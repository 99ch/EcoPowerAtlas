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

    def validate(self, attrs):
        latitude = attrs.get('latitude', getattr(self.instance, 'latitude', None))
        longitude = attrs.get('longitude', getattr(self.instance, 'longitude', None))
        head = attrs.get('head_m', getattr(self.instance, 'head_m', None))
        storage = attrs.get('storage_capacity_mwh', getattr(self.instance, 'storage_capacity_mwh', None))

        if latitude is not None and not (-90 <= float(latitude) <= 90):
            raise serializers.ValidationError({'latitude': 'La latitude doit être comprise entre -90 et 90.'})
        if longitude is not None and not (-180 <= float(longitude) <= 180):
            raise serializers.ValidationError({'longitude': 'La longitude doit être comprise entre -180 et 180.'})
        if head is not None and float(head) < 0:
            raise serializers.ValidationError({'head_m': 'Le dénivelé doit être positif.'})
        if storage is not None and float(storage) < 0:
            raise serializers.ValidationError({'storage_capacity_mwh': 'La capacité de stockage doit être positive.'})

        return attrs


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

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError('La valeur doit être positive.')
        return value

    def validate_year(self, value):
        if value and (value < 1900 or value > 2100):
            raise serializers.ValidationError('L’année doit être comprise entre 1900 et 2100.')
        return value


class ClimateSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClimateSeries
        fields = '__all__'
