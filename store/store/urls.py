"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings  # если "from store import settings" это аналогичный способ, но не все настройки подтягиваются 

# from products.views import index
from products.views import IndexView

from rest_framework.authtoken import views  # 12.7

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # path('', index, name='index'), 7.3
    path('products/', include('products.urls', namespace='products')),  # 4.2 добавили include() https://metanit.com/python/django/3.6.php
    path('users/', include('users.urls', namespace='users')),  # урок 4.7 добавили path('users/'.....
    path('accounts/', include('allauth.urls')),  # 8.4

    path('api/', include('api.urls', namespace='api')),  # 12.4
    path('api-token-auth/', views.obtain_auth_token),  # 12.7

]

if settings.DEBUG:  # DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # навести на static и подсказка покажет: какие импорты добавить и что передать в ф-ию static
