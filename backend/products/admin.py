from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'name', 'category', 'vehicle_type', 'quantity']

admin.site.register(Product, ProductAdmin)