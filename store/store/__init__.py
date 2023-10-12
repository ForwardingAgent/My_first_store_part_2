from .celery import app as celery_app

__all__ = ('celery_app', )  # чтобы celery стартануло вместе с приложением django
