from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required  # 5.5 не позволяет отрабатывать контроллеру пока не произведена авторизация (неавториз user не может добавить в корзину или зайти на страницу профайла пока не авторизирован)

from django.views.generic.base import TemplateView  # 7.3
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView  # 7.5


from products.models import ProductCategory, Product, Basket
from users.models import User
from django.core.paginator import Paginator


class IndexView(TemplateView):  # 7.3 в названии лучше использовать слово View чтобы было понятно что это из Views.py
    #  TemplateView наследуется от TemplateResponseMixin, ContextMixin, View
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):  # get_context_data можно использовать т.к. наследуется от ContextMixin
        context = super(IndexView, self).get_context_data()  # cоздает словарь | строка нужна для сохранения функционала метода родительского класса, так как мы его переопределили.
        context['title'] = 'Store'  # дополняем словарь своими данными
        return context


# def index(request):  # функция = контроллер = вьюха   ---комм. 7.3
#     context = {'title': 'Store'}
#     return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):  # приходит request это title или products или categories. C 6.2 добавили category_id. С 6.3 добавили page=1

    if category_id:  # 6.2
        category = ProductCategory.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    per_page = 3  # сколько товаров на странице
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)  # обращаемся к переменной paginator и через page передаем номер страницы товары которой надо отобразить, изначально 1 и первые 3 товара, стр.2-след. 3 товара
    #  products_paginator - тот же products только расширен методами для работы с Paginator()
    
    context = {
        'title': 'Store - Каталог',
        # 'products': Product.objects.all(), 6.2 изменяем т.к. products будет меняться из условия выбора выше в зависимости от category_id
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,  # 6.3
    }
    return render(request, 'products/products.html', context)
    # render - объединяем заданный шаблон html с заданным контекстным словарем и возвращаем объект HttpResponse с этим визуализированным кодом.


# 7.5 для basket_add и basket_remove нет смясла делать через классы т.к. код практически копируется
# class BasketCreateView(CreateView):
#     model = Basket  # от какой модели наследуемся
# 
#     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#       product = Product.objects.get(id=self.kwargs.get('product_id'))
#       basket = Basket.objects.filter(user=request.user, product=product)
#       if not basket.exists():
#       ........
#       return super().post(request, *args, **kwargs)


@login_required  # декоратор 5.5, можно тут прописать (login_url='/users/login/')чтобы перенаправлять на регистрацию, но пропишем это все в settings внизу
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():  # если корзина пуста то для user, устанавливаем для product кол-во = 1 
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.first()  # иначе товар в корзине увеличиваем на 1 и сохраняем
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required  # декоратор 5.5, можно тут прописать (login_url='/users/login/') чтобы перенаправлять на регистрацию, но пропишем это все в settings внизу
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
