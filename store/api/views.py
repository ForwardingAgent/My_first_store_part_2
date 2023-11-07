# from rest_framework.generics import ListAPIView  # 12.4 API Guide-Generic Views-ListAPIView  ListAPIView - класс только для чтения, предоставляет GET запрос
from rest_framework.viewsets import ModelViewSet  # 12.6 Api Guide-Viewsets-Modelviewset меняем ListAPIView на Modelviewset т.к. он наследуется от 5 различных классов
# from rest_framework.permissions import IsAuthenticatedOrReadOnly  # 12.7, в 12.7 на IsAdminUser
from rest_framework.permissions import IsAdminUser

from products.models import Product
from products.serializers import ProductSerializer


class ProductModelViewSet(ModelViewSet):  # 12.6 ModelViewSet - имеет кроме GET еще 5 вариантов .list(), .create(), ....
    queryset = Product.objects.all()  # предоставляем все объекты (наши товары)
    serializer_class = ProductSerializer  # указываем с каким сериалайзром будем работать - ProductSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )  # 12.7, позже расширяя IsAdminUser создаем свой

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):  # action приходит в запросе GET, POST, DELETE и тд
            self.permission_classes = (IsAdminUser, )
        return super(ProductModelViewSet, self).get_permissions()


# 12.6 убрали тк используем ModelViewSet
# class ProductListAPIView(ListAPIView):  # 12.4
#     queryset = Product.objects.all()  # предоставляем все объекты (наши товары)
#     serializer_class = ProductSerializer  # указываем с каким сериалайзром будем работать - ProductSerializer
