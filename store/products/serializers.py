from rest_framework import serializers  # 12.4

from products.models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):  # 12.4
#  12.5 в category хотим отображать не id=1,2... а название категории идем API Guide - Serializer relations - SlugRelatedField  (relations т.к. у нас отношения м/у category и product)
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())  # category - название той категории, slug_field - название которое хотим отображать (name, price...)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')  # можно, но не жел-но вместо кортежа '__all__' но могут подтянуться поля которые не нужны

#  API Guide - Pagination - Setting the pagination style, добавили в сеттингс, а можно добавить как класс
