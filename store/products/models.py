from django.db import models
# models - таблицы для БД
from users.models import User


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
    image = models.ImageField(upload_to='products_images')  # загружай images в папку products_images (создаст автоматом)
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
