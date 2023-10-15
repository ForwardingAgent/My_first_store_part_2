from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, OrderListView, OrderDetailView

# тут хорошо описано https://metanit.com/python/django/3.6.php
app_name = 'orders'

# 10.2
urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),  # 10.9
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),  # 10.10
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
