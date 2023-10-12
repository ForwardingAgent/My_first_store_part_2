import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store')
app.config_from_object('django.conf:settings', namespace='CELERY')  # senior не знает
app.conf.broker_url = settings.CELERY_BROKER_URL  # senior 
app.autodiscover_tasks()  # чтобы celery автоматич смотрел по всем папкам и иcкал tasks
