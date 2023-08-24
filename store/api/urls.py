from django.urls import path, include

# from api.views import ProductListAPIView  # 12.4
from api.views import ProductModelViewSet  # 12.6

from rest_framework import routers  # 12.6  

app_name = 'api'

router = routers.DefaultRouter()  # 12.6 т.к. у нас в views.py ModelViewSet c несколькими методами (list(), .create(), ....) то нужно прописать path для всех
router.register(r'products', ProductModelViewSet)  # 12.6 регистрируем наш класс | (r'.....') глобальное название для urls адресов

urlpatterns = [
    path('', include(router.urls)),  # GET .../api/product_list/
]

# urlpatterns = [  12.6 убрали тк  используем ProductModelViewSet
#     path('product-list/', ProductListAPIView.as_view(), name='product_list'),  # GET .../api/product_list/
# ]
# обязательно зарегистрировать в главном store/urls.py
