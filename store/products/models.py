import stripe
from collections.abc import Iterable

from django.db import models
from users.models import User

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY  # 10.7


class ProductCategory(models.Model):  # 3.3 3:10 models.Model этот класс позволяет класс Python перенести на SQL язык 
    name = models.CharField(max_length=128)  # 3.3 класс CharField говорит что переменная 'name' это строка с определенным набором символов
    description = models.TextField(null=True, blank=True)  # 3.3 TextField говорит что переменная 'description' строка с большим текстом, null-может быть пустым

    class Meta:  # 6.4  замена англ. слов в разделах на русские
        verbose_name = 'категория'
        verbose_name_plural = 'категория'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', blank=True)  # загружай images в папку products_images (создаст автоматом)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)  # 10.7 поле хранит id для системы оплаты
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    # связываем category (через класс ForeignKey) с другим классом ProductCategory
    # класс CASCADE - удаление категории и всех вложеных (категорий и продуктов)
    # класс PROTECT - удаляет только категорию
    # класс SET_DEFAULT (+ значение которое впечатывается по умолчанию при удалении)

    class Meta:  # 6.4  замена англ слов в разделах на русские
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    # 10.7 ОСНОВНОЙ МЕТОД Models это save, СРАБАТЫВАЕТ ВСЕГДА для сохранения объектов в БД, тут его переопределяем
    # если у нового продукта нет stripe_product_price (id для stripe) то отправляем его в create_stripe_product_price() и создаем
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        return super().save(force_insert, force_update, using, update_fields)

    def create_stripe_product_price(self):  # 10.7 делаем API для Stripe, заполняем БД в stripe
        stripe_product = stripe.Product.create(name=self.name)  # создаем продукт
        stripe_product_price = stripe.Price.create(  # заполняем необходимые по документации данные для БД в stripe
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency="rub",
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):  # 5.4 переопределяем QuerySet, добавляем два своих метода в QuerySet. Считает общее кол-во товаров и сумму каждого в корзине
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestap = models.DateTimeField(auto_now_add=True)  # в админке зафиксировать дату добавления заказа в корзине

    objects = BasketQuerySet.as_manager()  # 5.4

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):  # 5.4
        return self.product.price * self.quantity

    def de_json(self):  # 10.8
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
