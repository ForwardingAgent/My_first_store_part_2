from typing import Any
from django.db.models.query import QuerySet
import stripe

# 10.5
# from django.views.generic.base import TemplateView  # можно подставить ниже в class ...(TemplateView) для проверки шаблона
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt  # 10.6
from django.http import HttpResponse

from common.views import TitleMixin
from orders.forms import OrderForm
from products.models import Basket
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/cancled.html'


class OrderListView(TitleMixin, ListView):  # 10.9
    template_name = 'orders/orders.html'
    title = "Store - Заказы"
    queryset = Order.objects.all()
    ordering = ('-id')

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):  # 10.10
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    # у CreateView есть post - вызываем его для переопределения. Создается объект order и расширяем чз создание формы для перенаправления на оплату
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        line_items = []  # эту и 6 строк ниже можно убрать в models в class BasketQuerySet  10.7
        for basket in baskets:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            # line_items - это то что должно формироваться из заказа (вещи, кол-во, цена)
            line_items=line_items,  # заменил нижний словарь из документации на автоматом создающийся line_items выше
            # line_items = {
                #     # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                #     'price': 'price_1O0kWxGjuU4rp3qHSBW3Nozo',  # сформировал вручную id заказа в документации Stripe https://stripe.com/docs/checkout/quickstart?lang=python
                #     'quantity': 1,
                # },
            metadata={'order_id': self.object.id},  # 10.6 добавил metadata, она приходит в ответе от Stripe после оплаченого товара, добавляем то что хотим получить, в данном случае id заказа. Ловим его ниже в def fulfill_order.
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


# все ниже из документации Stripe https://stripe.com/docs/payments/checkout/fulfill-orders
@csrf_exempt  # 10.6  уберает необходимость передавать csrf-токен
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = event['data']['object']
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session
        # Fulfill the purchase...
        fulfill_order(line_items)

    # Passed signature verification
    return HttpResponse(status=200)

# stripe_webhook_view который выше возвращает оплаченый заказ
# в fulfill_order меняем status, заполняем basket_history(из продуктов которые пришли в оплаченом заказе), удаляем корзину товаров тк она уже куплена
def fulfill_order(line_items):
    order_id = int(line_items.metadata.order_id)  # 10.6 14.00 из session берем order_id
    order = Order.objects.get(id=order_id)  # 10.8  берем заказ после оплаты
    order.update_after_payment()  # 10.8 обновляем этот заказ
    # print("Fulfilling order")
