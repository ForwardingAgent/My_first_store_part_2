from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required  # 5.5 не позволяет отрабатывать контроллеру пока не произведена авторизация (неавториз user не может добавить в корзину или зайти на страницу профайла пока не авторизирован)

from products.models import ProductCategory, Product, Basket
from users.models import User
from django.core.paginator import Paginator


def index(request):  # функция = контроллер = вьюха
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)


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



'''        'products': [
            {
                'image': '/static/vendor/img/products/Adidas-hoodie.png',
                'name': 'худи черного цвета с монограммами adidas Originals',
                'price': str(6090),
                'description': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни',
            },
            {
                'image': '/static/vendor/img/products/Blue-jacket-The-North-Face.png',
                'name': 'Синяя куртка The North Face',
                'price': str(23725),
                'description': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.',
            },
            {
                'image': '/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png',
                'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
                'price': str(3390),
                'description': 'Материал с плюшевой текстурой. Удобный и мягкий.',
            },
            {
                'image': '/static/vendor/img/products/Black-Nike-Heritage-backpack.png',
                'name': 'Черный рюкзак Nike Heritage',
                'price': str(2340),
                'description': 'Плотная ткань. Легкий материал.',
            },
            {
                'image': '/static/vendor/img/products/Black-Dr-Martens-shoes.png',
                'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
                'price': str(13590),
                'description': 'Гладкий кожаный верх. Натуральный материал.',
            },
            {
                'image': '/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png',
                'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
                'price': str(2890),
                'description': 'Легкая эластичная ткань сирсакер Фактурная ткань.',
            }
        ]
    }
    return render(request, 'products/products.html', context)'''
