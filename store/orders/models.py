from django.db import models

from users.models import User
from products.models import Basket


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):  # 10.8 берем корзину после прошедшей оплаты чтобы сохранить в истории и обновить статус заказа
        print(self.initiator, self.status)
        baskets = Basket.objects.filter(user=self.initiator)  # берем пользователя который все оформлял
        self.status = self.PAID
        self.basket_history = {  # (в админке все детали заказа) по ключу purchased_items будем хранить список из словарей которые образуются в de_json (для каждого продукта свой)
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),  # вывести общую сумму товаров
        }
        baskets.delete()  # после оплаты и изменений корзина не нужна
        self.save()  # и сохраняем все изменения (status, basket_history)
