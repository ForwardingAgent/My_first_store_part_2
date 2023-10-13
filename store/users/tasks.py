from store.celery import shared_task
from store.celery import app  # senior
import time

from users.models import User, EmailVerification

import uuid
from datetime import timedelta
from django.utils.timezone import now


@shared_task
def test_task():
    time.sleep(20)
    print('Hello from test_task')


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(
        code=uuid.uuid4(),
        user=user,
        expiration=expiration
    )
    record.send_verification_email()
