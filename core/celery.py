import os
from celery import Celery
from celery.schedules import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # revalida as certidoes a cada 24hr
    'revalidate-certificates-every-day': {
        'task': 'mercatorio.tasks.revalidate_certificates',
        'schedule': schedule(86400.0),
    },
}
