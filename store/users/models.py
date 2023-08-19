from django.db import models
from django.contrib.auth.models import AbstractUser

# 4.6 урок
class User(AbstractUser):  # AbstractUser(models.Model) наследуется от models.Model. Берем User(AbstractUser), а не User(models.Model) т.к. в AbstractUser уже созданы все поля для user'a, a если от models.Model то надо все поля создавать самому
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # можно добавить поле пол, день рождения и тд
    # после работы с моделями всегда makemigrations!!
