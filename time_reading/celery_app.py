import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'time_reading.settings')

app = Celery('time_reading')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'my-scheduled-task': {
        'task': 'time_reading_system.tasks.statistics_total_reading_time',
        'schedule': crontab(minute=1),
    },
}


