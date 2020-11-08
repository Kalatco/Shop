from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from products.models import (
    Category,
    Product,
    Image,
    Customer,
    Order,
    OrderProduct,
    ProductSize,
    Size
)
from django.forms import TextInput, Textarea
from django.shortcuts import redirect
from django.db import models

admin.site.site_header = "StickerShop Admin"
admin.site.site_header = "StickerShop Admin Portal"
admin.site.index_title = "StickerShop"
admin.site.unregister(User)
admin.site.unregister(Group)


class ProductInline(admin.TabularInline):
    model = Product
    readonly_fields = ('name', 'description')
    can_delete = False
    max_num=0


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    search_fields= ('name', )
    list_display = ('name', )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={ 'rows': 2, 'cols': 100 })},
    }

    inlines = [
        ProductInline,
    ]

    def has_delete_permission(self, request, obj=None):
        return False


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image_preview


class SizeAdmin(admin.ModelAdmin):
    model = Size

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={ 'rows': 2, 'cols': 100 })},
    }


class ProductSize(admin.TabularInline):
    model = ProductSize


class ProductAdmin(admin.ModelAdmin):
    model = Product
    search_fields= ('name', 'category')
    list_display = ('name', 'category')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={ 'rows': 4, 'cols': 100 })},
    }

    inlines = [
        ImageInline,
        ProductSize,
    ]

    def has_delete_permission(self, request, obj=None):
        return False


class OrderInline(admin.TabularInline):
    model = Order
    readonly_fields = ('total_cost', 'status', 'tracking')
    can_delete = False
    max_num=0


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    search_fields= ('first_name', 'last_name', 'email')
    list_display = ('first_name', 'last_name', 'email')
    readonly_fields = ('first_name', 'last_name', 'email', 'address', 'appartment', 'city', 'state', 'country', 'zip_code', 'phone')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={ 'rows': 2, 'cols': 100 })},
    }

    inlines = [
        OrderInline,
    ]

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
    

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product', 'order', 'quantity', 'cost')
    can_delete = False
    max_num=0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    search_fields= ('customer', 'status')
    list_display = ('customer', 'status')
    fields = ('total_cost', 'status', 'customer_first_name', 'customer_email', 'customer_address', 'customer_phone')
    readonly_fields = ('total_cost', 'customer_first_name', 'customer_email', 'customer_address', 'customer_phone')

    inlines = [
        OrderProductInline,
    ]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={ 'rows': 2, 'cols': 100 })},
    }

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False


admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
