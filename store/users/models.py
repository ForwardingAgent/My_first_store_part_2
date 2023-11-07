from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now

# 4.6


class User(AbstractUser):  # AbstractUser(models.Model) наследуется от models.Model. Берем User(AbstractUser), а не User(models.Model) т.к. в AbstractUser уже созданы все поля для user'a, a если от models.Model то надо все поля создавать самому
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # можно добавить поле пол, день рождения и тд
    # после работы с моделями всегда makemigrations!!
    is_verified_email = models.BooleanField(default=False)  # 7.10 после подтверждения email будет True


class EmailVerification(models.Model):  # 7.10
    code = models.UUIDField(unique=True)  # при регистрации user генерирует уникальную ссылку для него
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)  # связыаем EmailVerification с user
    created = models.DateTimeField(auto_now_add=True)  # created будет заполняться автоматом когда создан объект
    expiration = models.DateTimeField()  # когда заканчивается срок действия ссылки

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification',
                       kwargs={'email': self.user.email,
                               'code': self.code
                               })  # 7.11
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для одтверждение учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        # return True if now() >= self.expiration else False  в уроке
        return now() >= self.expiration  # сам исправил
