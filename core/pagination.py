from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Expose a consistent page size with opt-in overrides."""

    page_size = getattr(settings, 'API_DEFAULT_PAGE_SIZE', 50)
    page_size_query_param = 'page_size'
    max_page_size = getattr(settings, 'API_MAX_PAGE_SIZE', 200)
    page_query_param = 'page'
