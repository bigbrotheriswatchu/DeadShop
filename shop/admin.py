from django.contrib import admin
from shop.models import *

class CollectionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Collection._meta.fields]

    class Meta:
        model = ProductInOrder


admin.site.register(Collection, CollectionAdmin)

class TshirtAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tshirt._meta.fields]

    class Meta:
        model = ProductInOrder


admin.site.register(Tshirt, TshirtAdmin)

class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0


class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status


admin.site.register(Status, StatusAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]

    class Meta:
        model = ProductInOrder


admin.site.register(ProductInOrder, ProductInOrderAdmin)


class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
        model = ProductInBasket


admin.site.register(ProductInBasket, ProductInBasketAdmin)
