from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings  # если "from store import settings" это аналогичный способ, но не все настройки подтягиваются

# from products.views import index
from products.views import IndexView
from orders.views import stripe_webhook_view

from rest_framework.authtoken import views  # 12.7

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # path('', index, name='index'), 7.3
    path('products/', include('products.urls', namespace='products')),  # 4.2 добавили include() https://metanit.com/python/django/3.6.php
    path('users/', include('users.urls', namespace='users')),  # урок 4.7 добавили path('users/'.....
    path('accounts/', include('allauth.urls')),  # 8.4 регистрация чз соцсети (github)
    path('orders/', include('orders.urls', namespace='orders')),  # 10.2
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),  # 10.6

    path('api/', include('api.urls', namespace='api')),  # 12.4
    path('api-token-auth/', views.obtain_auth_token),  # 12.7
]

if settings.DEBUG:  # DEBUG == True:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # навести на static и подсказка покажет: какие импорты добавить и что передать в ф-ию static
