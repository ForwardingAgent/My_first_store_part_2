from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailVerification


class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:  # setUp встроенная в TestCase функция, чтобы создавать переменные и дальше использовать в тестах. Создаем self.products и ниже использовать в функциях
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Nik', 'last_name': 'Nik',
            'username': 'user1', 'email': 'mail1@mail.com',
            'password1': 'QWErty123!', 'password2': 'QWErty123!',
        }

    def test_user_registration(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):

        response = self.client.post(self.path, self.data)

        username = self.data['username']
        # проверяем создание user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # проверяем на создание email_verification
        email_verification = EmailVerification.objects.filter(user__username=username)  # user__username - Обращение из вторичной модели "EmailVerification" к первичной "User"  по внешнему ключу "user" (т.н. метод обратной связи)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        username = self.data['username']
        user = User.objects.create(username=username)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.Ok)
        self.assertContains(response, 'Пользователь с таким именем уже существует', html=True)
