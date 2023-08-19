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

from products.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', include('products.urls', namespace='products')),  # урок 4.2 добавили include() https://metanit.com/python/django/3.6.php
    path('users/', include('users.urls', namespace='users')),  # урок 4.7 добавили path('users/'.....
]

if settings.DEBUG:  # DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # навести на static и подсказка покажет: какие импорты добавить и что передать в ф-ию static
