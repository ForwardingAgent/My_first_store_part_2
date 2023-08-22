from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail

# 4.6 урок
class User(AbstractUser):  # AbstractUser(models.Model) наследуется от models.Model. Берем User(AbstractUser), а не User(models.Model) т.к. в AbstractUser уже созданы все поля для user'a, a если от models.Model то надо все поля создавать самому
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # можно добавить поле пол, день рождения и тд
    # после работы с моделями всегда makemigrations!!
    is_verified_email = models.BooleanField(default=False)  # 7.10 после подтверждения email будет True


class EmailVerification(models.Model):  # 7.10
    code = models.UUIDField(unique=True)  # при регистрации н=генерирует уникальную ссылку для него
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)  # связыаем EmailVerification с user
    created = models.DateTimeField(auto_now_add=True)  # created будет заполняться автоматом когда создан объект
    expiration = models.DateTimeField()  # когда заканчивается срок действия ссылки

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        send_mail(
            "Subject here",
            "MY test verification email!",
            "from@example.com",
            [self.user.email],
            fail_silently=False,
        )
