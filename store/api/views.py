# from rest_framework.generics import ListAPIView  # 12.4 API Guide-Generic Views-ListAPIView  ListAPIView - класс только для чтения, предоставляет GET запрос
from rest_framework.viewsets import ModelViewSet  # 12.6 Api Guide-Viewsets-Modelviewset меняем ListAPIView на Modelviewset т.к. он наследуется от 5 различных классов


from products.models import Product
from products.serializers import ProductSerializer


class ProductModelViewSet(ModelViewSet):  # 12.6 ModelViewSet - имеет кроме GET еще 5 вариантов .list(), .create(), ....
    queryset = Product.objects.all()  # предоставляем все объекты (наши товары)
    serializer_class = ProductSerializer  # указываем с каким сериалайзром будем работать - ProductSerializer


# 12.6 убрали тк используем ModelViewSet
# class ProductListAPIView(ListAPIView):  # 12.4 
#     queryset = Product.objects.all()  # предоставляем все объекты (наши товары)
#     serializer_class = ProductSerializer  # указываем с каким сериалайзром будем работать - ProductSerializer
