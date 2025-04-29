from django.contrib import admin
from .models import Product, Hurley, Grip, Sliotar, Helmet
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for the Product model.
    """
    list_display = ('name', 'category', 'price', 'stock')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    ordering = ('name',)


@admin.register(Hurley)
class HurleyAdmin(admin.ModelAdmin):
    """
    Admin interface for the Hurley model.
    """
    list_display = ('product', 'grip_color', 'weight', 'size')
    search_fields = ('product__name', 'grip_color')
    ordering = ('product__name',)
    list_filter = ('weight', 'size')


@admin.register(Grip)
class GripAdmin(admin.ModelAdmin):
    """
    Admin interface for the Grip model.
    """
    list_display = ('product', 'grip_color')
    search_fields = ('product__name', 'grip_color')
    ordering = ('product__name',)


@admin.register(Sliotar)
class SliotarAdmin(admin.ModelAdmin):
    """
    Admin interface for the Sliotar model.
    """
    list_display = ('product', 'color')
    search_fields = ('product__name', 'color')
    ordering = ('product__name',)


@admin.register(Helmet)
class HelmetAdmin(admin.ModelAdmin):
    """
    Admin interface for the Helmet model.
    """
    list_display = ('product', 'size', 'color')
    search_fields = ('product__name', 'size', 'color')
    ordering = ('product__name',)
