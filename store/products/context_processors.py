from products.models import Basket


def baskets(request):  # 7.13
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}  # далее подключаем в settings
