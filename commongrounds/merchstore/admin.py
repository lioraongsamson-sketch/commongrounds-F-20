from django.contrib import admin

from .models import Product, ProductType


class ProductIngredientInLine(admin.TabularInline):
    model = Product


class ProductAdmin(admin.ModelAdmin):
    model = ProductType
    inlines = [ProductIngredientInLine,]


admin.site.register(ProductType, ProductAdmin)
# Register your models here.
