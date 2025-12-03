from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('countries', views.CountryViewSet)
router.register('regions', views.RegionViewSet)
router.register('datasets', views.EnergyDatasetViewSet)
router.register('hydro-sites', views.HydroSiteViewSet)
router.register('resource-metrics', views.ResourceMetricViewSet)
router.register('climate-series', views.ClimateSeriesViewSet)

urlpatterns = router.urls
