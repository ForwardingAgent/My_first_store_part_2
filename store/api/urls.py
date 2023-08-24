from django.urls import path

from api.views import ProductListAPIView  # 12.4

app_name = 'api'

urlpatterns = [
    path('product-list/', ProductListAPIView.as_view(), name='product_list'),  # GET .../api/product_list/
]
# обязательно зарегистрировать в главном store/urls.py
