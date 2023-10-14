from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView

# тут хорошо описано https://metanit.com/python/django/3.6.php
app_name = 'orders'

# 10.2
urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
