import os
import time

from celery import Celery, shared_task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store')
app.config_from_object('django.conf:settings', namespace='CELERY')  # namespace='CELERY' все настройки для Celery будут искаться с префиксом CELERY_ типа CELERY_BROKER_URL или CELERY_RESULT_BACKEND
app.conf.broker_url = settings.CELERY_BROKER_URL      # senior
app.autodiscover_tasks()  # celery автоматич смотрел по всем папкам и иcкал tasks


# @shared_task
# def test_task():
#     time.sleep(20)
#     print('Hello from test_task')
