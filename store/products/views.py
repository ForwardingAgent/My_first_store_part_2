from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required  # 5.5 не позволяет отрабатывать контроллеру пока не произведена авторизация (неавториз user не может добавить в корзину или зайти на страницу профайла пока не авторизирован)

from django.views.generic.base import TemplateView  # 7.3
from django.views.generic.list import ListView  # 7.4
from django.views.generic.edit import CreateView  # 7.5

from products.models import ProductCategory, Product, Basket
from common.views import TitleMixin  # 7.8

from users.models import User
from django.core.paginator import Paginator


class IndexView(TitleMixin, TemplateView):  # 7.8 TitleMixin, 7.3 в названии лучше использовать слово View чтобы было понятно что это из Views.py
    #  TemplateView наследуется от TemplateResponseMixin, ContextMixin, View
    template_name = 'products/index.html'
    title = 'Store'  # 7.8


    # 7.8 def get_context_data(self, **kwargs) -> Dict[str, Any]:  # get_context_data можно использовать т.к. наследуется от ContextMixin
    #     context = super(IndexView, self).get_context_data(**kwargs)  # cоздает словарь | сначала через super вызываем родительский метод, чтобы он выполнился, и ниже добавляем наши ключи в словарь (т.е. переопределили род.метод)
    #     context['title'] = 'Store'  # дополняем словарь своими данными
    #     return context


class ProductListView(TitleMixin, ListView):  # 7.4 ListView класс отвечающий за вывод списка объектов
    model = Product  # с какой моделью работаем
    template_name = 'products/products.html'  # с каким шаблоном работаем
    paginate_by = 3
    title = 'Store - Каталог'  # 7.8

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(ProductListView, self).get_queryset()  # тут формируется queryset=Product.objects.all()
        category_id = self.kwargs.get('category_id')  # category_id приходит из products/urls.py path('category/<int:category_id>/ и хранится в self.kwargs | при первом переходе (когда нужно показать все категории) self.kwargs.get(category_id) выдаст None, просто self.kwargs['category_id'] - ошибку
        return queryset.filter(category_id=category_id) if category_id else queryset  # если category_id не None от возвращаем категорию, иначе весь список (при первом переходе)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductListView, self).get_context_data(**kwargs)  # сначала через super вызываем родительский метод, чтобы он выполнился, и ниже добавляем наши ключи в словарь (т.е. переопределили род.метод)
        context['categories'] = ProductCategory.objects.all()  # добавились категории в сайдбар
        # context['title'] = 'Store - Каталог'  # 7.8 перенесли в class
        return context


# 7.5 для basket_add и basket_remove нет смысла делать через классы т.к. код практически копируется
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
