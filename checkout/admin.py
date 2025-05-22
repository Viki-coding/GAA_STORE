from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for the Order model.
    """
    list_display = (
        'order_number', 'user_profile', 'order_date', 'status', 'grand_total')
    list_filter = (
        'status', 'payment_status', 'delivery_status')
    search_fields = (
        'order_number',
        'user_profile__user__username',
        'user_profile__user__email')
    readonly_fields = (
        'order_number', 'order_date',
        'total_price',
        'delivery_cost',
        'grand_total')
    fieldsets = (
        (None, {
            'fields': (
                'order_number',
                'user_profile',
                'shipping_address',
                'order_date',
                'status')
        }),
        ('Payment & Delivery', {
            'fields': (
                'payment_status',
                'delivery_status',
                'delivery_cost',
                'grand_total')
        }),
        ('Gift Options', {
            'fields': ('is_gift', 'gift_message')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'lineitem_total')
    search_fields = ('order__order_number', 'product__name')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'full_name', 'eircode', 'country')
    search_fields = ('user_profile__user__username', 'full_name', 'eircode')
