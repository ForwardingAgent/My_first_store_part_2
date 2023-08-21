from django.urls import path

# from products.views import products, basket_add, basket_remove
from products.views import ProductListView, basket_add, basket_remove  # 7.4

# 4.2 урок, тут хорошо описано https://metanit.com/python/django/3.6.php
app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='category'),  # 6.2 ../products/category/<category_id>/
    path('page/<int:page>/', ProductListView.as_view(), name='paginator'),  # 6.3 ../products/paginator/<page_number>/ 7.4 /<int:page_number>/ меняем на /<int:page>/ тк в html и views используется page
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),  # 5.3 ../products/baskets/add/<product_id>
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),  # 5.3
]
