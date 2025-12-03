import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecopoweratlas.settings')

app = Celery('ecopoweratlas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):  # pragma: no cover - utility for quick checks
    print(f'Request: {self.request!r}')
