from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory

#  !!!!!нужно зайти в контейнер приложения!!!!! и запуск тестов через './manage.py test products.tests.ProductsListViewTestCase.test_list'
class IndexViewTestCase(TestCase):

    def test_view(self):  # все методы должны начинаться с test...
        path = reverse('index')  # присваиваем адрес http://127.0.0.1:8000/
        response = self.client.get(path)  # в TestCase встроен client(), client это класс который помогает обращаться к различным методам get, put...
        # тут запрашиваем главную страницу через client.get(path)
        print(response)
        # сравниваем объекты из response c тем что хотим получить
        self.assertEqual(response.status_code, HTTPStatus.OK)  # статусы сравнивать не с цифрой 200, 201.. а с HTTPStatus
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')  # проверяем тот ли шаблон


class ProductsListViewTestCase(TestCase):  # 9.4
    fixtures = ['categories.json', 'goods.json']  # тк при тесте создается пустая БД нужно ее заполнить

    def setUp(self):  # setUp встроенная в TestCase функция, чтобы создавать переменные и дальше использовать в тестах. Создаем self.products и ниже использовать в функциях
        self.products = Product.objects.all()  # создаем переменную для того чтобы сравнить с ней

    def test_list(self):
        path = reverse('products:index')  # присваиваем адрес главной страницы
        response = self.client.get(path)

        # products = Product.objects.all()  # создаем переменную для того чтобы сравнить с ней | убираем тк она создана в def setUp
        # self.assertEqual(response.status_code, HTTPStatus.OK)  # сравниваем объекты из response c тем что хотим получить
        # self.assertEqual(response.context_data['title'], 'Store - Каталог')
        # self.assertTemplateUsed(response, 'products/products.html')
        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']), 
            list(self.products[:3])
        )  # два одинаковых с виду quryset не равны м/у собой (т.к. сделаны в разное время), делаем их списками и сравниваем

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})  # присваиваем адрес как в products/urls | kwargs или можно args перечисляем переменные в ('', '',)
        response = self.client.get(path)

        # products = Product.objects.all()  # | убираем тк она создана в def setUp
        # self.assertEqual(response.status_code, HTTPStatus.OK)  # сравниваем объекты из response c тем что хотим получить
        # self.assertEqual(response.context_data['title'], 'Store - Каталог')
        # self.assertTemplateUsed(response, 'products/products.html')
        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )  # два одинаковых с виду quryset не равны м/у собой (т.к. сделаны в разное время), делаем их list и сравниваем

    def _common_tests(self, response):  # DRY, убрали блоки из test_list и test_list_with_category в одну ф-ю _common_tests
        self.assertEqual(response.status_code, HTTPStatus.OK)  # сравниваем объекты из response c тем что хотим получить
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
