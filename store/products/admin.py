from django.contrib import admin
# Register your models here.

from products.models import ProductCategory, Product, Basket


# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)  # 6.4 нужно передать модель с которой будем работать (Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')  # отвечает за то как я хочу видеть все продукты на гл.странице, сейчас строка из products/models.py def __str__(self)...
    fields = ('name', 'description', 'price', 'quantity', 'image', 'category')  # порядок можно менять и поменяются в admin'ке | кортеж в кортеже тогда два значения на одной линии
    readonly_fields = ('description',)  # делает поле неизменяемым
    search_fields = ('name',)  # добавляет поле поиска
    ordering = ('name',)  # отображение списка в алфавитном порядке | ('-name') в обратном алфав порядке


class BasketAdmin(admin.TabularInline):  # 6.4 TabularInline можно добавлять если есть ForeignKey (тут Basket связан с user в models). Добавялет в админке user'а внизу корзину Basket со всеми товарами
    model = Basket
    fields = ('product', 'quantity', 'created_timestap')
    readonly_fields = ('created_timestap',)  # неизменяемая дата добавления товара 
    extra = 0  # по умолчанию = 3 добавляет 3 доп.поля в добавленом разделе Basket у user'а в админке, ставим 0 чтоб полей небыло
