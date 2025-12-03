import logging
from typing import Optional

from celery import shared_task
from django.utils import timezone

from . import models

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generate_metric_snapshot(self, country_iso3: Optional[str] = None) -> dict:
    """Dummy heavy task placeholder that aggregates metrics."""

    queryset = models.ResourceMetric.objects.select_related('country').all()
    if country_iso3:
        queryset = queryset.filter(country__iso3__iexact=country_iso3)

    total_metrics = queryset.count()
    totals = queryset.values('resource_type').order_by('resource_type')

    payload = {
        'country_iso3': country_iso3,
        'total_metrics': total_metrics,
        'resource_types': list(totals),
        'generated_at': timezone.now().isoformat(),
        'task_id': self.request.id,
    }
    logger.info('Generated metric snapshot', extra={'payload': payload})
    return payload
