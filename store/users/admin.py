from django.contrib import admin

from users.models import User, EmailVerification
from products.admin import BasketAdmin

# 4.6 регистрируем нашу модель User дополненую полем image
# admin.site.register(User)


#  6.4
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)  # отвечает за то как я хочу видеть все продукты на гл.странице, сейчас строка из products/models.py def __str__(self)...
    inlines = (BasketAdmin,)  # добавялет в админке user'а внизу корзину Basket со всеми товарами


@admin.register(EmailVerification)  # 7.10
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')  # выводится в таблице всех объектов
    fields = ('code', 'user', 'expiration', 'created')  # выводится в самом объекте
    readonly_fields = ('created',)  # тк создается автоматом в models EmailVerification то readonly_fields
