from rest_framework.generics import ListAPIView  # 12.4 API Guide-Generic Views-ListAPIView  ListAPIView - класс только для чтения, предоставляет GET запрос

from products.models import Product
from products.serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()  # предоставляем все объекты (наши товары)
    serializer_class = ProductSerializer  # указываем с каким сериалайзром будем работать - ProductSerializer
