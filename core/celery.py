from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from apps.common.services.logging import Telegram
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task():
    Telegram.send_log("Debug task")

app.conf.beat_schedule = {
    'update_currency_every_midnight': {
        'task': 'common.tasks.fetch_currency_rate',
        'schedule': crontab(hour=0, minute=0),
    },
}



