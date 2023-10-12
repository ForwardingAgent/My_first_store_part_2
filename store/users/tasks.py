# from celery import shared_task
from store.celery import app

from users.models import User, EmailVerification

import uuid
from datetime import timedelta
from django.utils.timezone import now


# @shared_task
@app.task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)  # сколько действует ссылка
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)  # uuid создает каждый раз уникальный код
    record.send_verification_email()
